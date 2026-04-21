import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import html2pdf from 'html2pdf.js';
import { GripVertical } from 'lucide-react';
import api from '../api/axios';
import './ResumeBuilder.css';

const ResumeBuilder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [resume, setResume] = useState(null);
  const [name, setName] = useState('');
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [designation, setDesignation] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [location, setLocation] = useState('');
  const [profileData, setProfileData] = useState({ experiences: [], educations: [], skills: [], projects: [], certifications: [], courses: [], achievements: [] });
  const [loading, setLoading] = useState(true);
  const [isPrinting, setIsPrinting] = useState(false);
  const [profileBio, setProfileBio] = useState('');
  
  // Drag and drop state
  const [draggingItem, setDraggingItem] = useState(null);
  const [dragOverSection, setDragOverSection] = useState(null);
  const [dragOverIndex, setDragOverIndex] = useState(null);
  const [canDrag, setCanDrag] = useState(false);
  
  const printRef = useRef();

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const [resRes, profRes] = await Promise.all([
        api.get(`/resume/${id}`),
        api.get('/profile')
      ]);
      setResume(resRes.data);
      setName(resRes.data.name || resRes.data.title || '');
      setTitle(resRes.data.title || '');
      setSummary(resRes.data.summary || '');
      setDesignation(resRes.data.designation || '');
      setEmail(resRes.data.email || '');
      setPhone(resRes.data.phone || '');
      setLocation(resRes.data.location || '');
      setProfileData({
        experiences: profRes.data.data.experiences || [],
        educations: profRes.data.data.educations || [],
        skills: profRes.data.data.skills || [],
        projects: profRes.data.data.projects || [],
        certifications: profRes.data.data.certifications || [],
        courses: profRes.data.data.courses || [],
        achievements: profRes.data.data.achievements || []
      });
      setProfileBio(profRes.data.data.profile?.bio || '');
    } catch (err) {
      console.error(err);
      if (err.response?.status === 404) navigate('/');
    } finally {
      setLoading(false);
    }
  };

  // --- Drag and Drop Handlers ---
  
  const handleDragStart = (e, item, type, index) => {
    // Robust Check: Only allow drag if the mouse was pressed on the handle
    if (!canDrag) {
      e.preventDefault();
      return;
    }
    setDraggingItem({ item, type, index });
    // Reset switch for next time
    setCanDrag(false);
  };

  const handleDragOver = (e, sectionType, index = null) => {
    e.preventDefault();
    // Only update state if something actually changed to prevent lag/stutter
    if (dragOverSection !== sectionType) {
      setDragOverSection(sectionType);
    }
    if (index !== null && dragOverIndex !== index) {
      setDragOverIndex(index);
    }
  };

  const handleDrop = async (e, targetSection, targetIndex) => {
    e.preventDefault();
    if (!draggingItem) return;

    const { item, type, index: sourceIndex } = draggingItem;
    
    // Reset states
    setDraggingItem(null);
    setDragOverSection(null);
    setDragOverIndex(null);

    // If dropped in a different section type, ignore
    if (type !== targetSection) return;
    
    // If dropped in the same position, ignore
    if (sourceIndex === targetIndex) return;

    // --- OPTIMISTIC UI: Reorder state immediately ---
    const listKey = type + 's';
    const items = [...resume[listKey]];
    const [movedItem] = items.splice(sourceIndex, 1);
    items.splice(targetIndex, 0, movedItem);

    // Update local state so it feels "instant"
    setResume(prev => ({
      ...prev,
      [listKey]: items
    }));

    // --- SYNC WITH BACKEND ---
    try {
      const orderedIds = items.map(i => i.id);
      const endpointMap = {
        experience: 'experience/order',
        skill: 'skill/order',
        education: 'education/order',
        project: 'project/reorder',
        certification: 'certification/reorder',
        course: 'course/reorder',
        achievement: 'achievement/reorder'
      };
      
      await api.put(`/resume/${id}/${endpointMap[type]}`, { ordered_ids: orderedIds });
      // fetchData() is called to ensure all IDs and orders are perfectly in sync with DB
      fetchData(); 
    } catch (err) {
      console.error('Reorder failed', err);
      fetchData(); // Rollback on failure
    }
  };

  const handleAddSkill = async (skill_id) => {
    try {
      const currentSkills = resume.skills || [];
      const order = currentSkills.length;
      await api.post(`/resume/${id}/skill`, { skill_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleRemoveSkill = async (skill_id) => {
    setResume(prev => ({
      ...prev,
      skills: prev.skills.filter(s => s.id !== skill_id)
    }));
    try {
      await api.delete(`/resume/${id}/skill/${skill_id}`);
    } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddExp = async (experience_id) => {
    try {
      const currentExps = resume.experiences || [];
      const order = currentExps.length;
      await api.post(`/resume/${id}/experience`, { experience_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleRemoveExp = async (experience_id) => {
    setResume(prev => ({
      ...prev,
      experiences: prev.experiences.filter(e => e.id !== experience_id)
    }));
    try {
      await api.delete(`/resume/${id}/experience/${experience_id}`);
    } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddEdu = async (education_id) => {
    try {
      const currentEdus = resume.educations || [];
      const order = currentEdus.length;
      await api.post(`/resume/${id}/education`, { education_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleRemoveEdu = async (education_id) => {
    setResume(prev => ({
      ...prev,
      educations: prev.educations.filter(e => e.id !== education_id)
    }));
    try { await api.delete(`/resume/${id}/education/${education_id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddProject = async (project_id) => {
    try {
      const current = resume.projects || [];
      const order = current.length;
      await api.post(`/resume/${id}/project`, { project_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };
  const handleRemoveProject = async (project_id) => {
    setResume(prev => ({
      ...prev,
      projects: prev.projects.filter(p => p.id !== project_id)
    }));
    try { await api.delete(`/resume/${id}/project/${project_id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddCert = async (certification_id) => {
    try {
      const current = resume.certifications || [];
      const order = current.length;
      await api.post(`/resume/${id}/certification`, { certification_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };
  const handleRemoveCert = async (certification_id) => {
    setResume(prev => ({
      ...prev,
      certifications: prev.certifications.filter(c => c.id !== certification_id)
    }));
    try { await api.delete(`/resume/${id}/certification/${certification_id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddCourse = async (course_id) => {
    try {
      const current = resume.courses || [];
      const order = current.length;
      await api.post(`/resume/${id}/course`, { course_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };
  const handleRemoveCourse = async (course_id) => {
    setResume(prev => ({
      ...prev,
      courses: prev.courses.filter(c => c.id !== course_id)
    }));
    try { await api.delete(`/resume/${id}/course/${course_id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddAchievement = async (achievement_id) => {
    try {
      const current = resume.achievements || [];
      const order = current.length;
      await api.post(`/resume/${id}/achievement`, { achievement_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };
  const handleRemoveAchievement = async (achievement_id) => {
    setResume(prev => ({
      ...prev,
      achievements: prev.achievements.filter(a => a.id !== achievement_id)
    }));
    try { await api.delete(`/resume/${id}/achievement/${achievement_id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleUpdateMetadata = async () => {
    if (!title.trim()) return;
    try {
      await api.put(`/resume/${id}`, { title, name, summary, designation, email, phone, location });
    } catch (err) {
      console.error('Failed to update resume metadata', err);
    }
  };

  const handleUseProfileBio = () => {
    if (!profileBio) {
      alert('No bio found in profile. Please set it in your Profile page.');
      return;
    }
    setSummary(profileBio);
  };

  const handleDownloadPdf = () => {
    const element = printRef.current;
    setIsPrinting(true);
    setTimeout(() => {
      const opt = {
        margin: 15,
        filename: `${(resume.title || 'Resume').replace(/\s+/g, '_')}_Resume.pdf`,
        image: { type: 'jpeg', quality: 1.0 },
        html2canvas: { scale: 3, useCORS: true, letterRendering: true, scrollX: 0, scrollY: 0 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
      };
      html2pdf().from(element).set(opt).save().then(() => {
        setIsPrinting(false);
      });
    }, 100);
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    if (dateStr === 'Present') return 'Present';
    return dateStr.split(' ')[0];
  };

  if (loading) return <div className="loading-screen">Loading Resume...</div>;
  if (!resume) return <div className="error-screen">Resume not found.</div>;

  const addedSkillIds = new Set((resume.skills || []).map(s => s.id));
  const addedExpIds = new Set((resume.experiences || []).map(e => e.id));
  const addedEduIds = new Set((resume.educations || []).map(e => e.id));
  const addedProjectIds = new Set((resume.projects || []).map(p => p.id));
  const addedCertIds = new Set((resume.certifications || []).map(c => c.id));
  const addedCourseIds = new Set((resume.courses || []).map(c => c.id));
  const addedAchievementIds = new Set((resume.achievements || []).map(a => a.id));

  const availableSkills = profileData.skills.filter(s => !addedSkillIds.has(s.id));
  const availableExps = profileData.experiences.filter(e => !addedExpIds.has(e.id));
  const availableEdus = profileData.educations.filter(e => !addedEduIds.has(e.id));
  const availableProjects = profileData.projects.filter(p => !addedProjectIds.has(p.id));
  const availableCerts = profileData.certifications.filter(c => !addedCertIds.has(c.id));
  const availableCourses = profileData.courses.filter(c => !addedCourseIds.has(c.id));
  const availableAchievements = profileData.achievements.filter(a => !addedAchievementIds.has(a.id));

  const getSectionClass = (type) => {
    if (!draggingItem) return "resume-section";
    if (dragOverSection === type) {
      return draggingItem.type === type ? "resume-section valid-drop" : "resume-section invalid-drop";
    }
    return "resume-section";
  };

  return (
    <div className="builder-container animate-fade-in">
      <div className="builder-header">
        <div className="builder-heading-group">
          <div className="builder-heading-label">Resume Heading</div>
          <input
            className="builder-heading-input"
            value={name}
            onChange={e => setName(e.target.value)}
            onBlur={handleUpdateMetadata}
            placeholder="e.g. Backend Dev Resume..."
          />
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn btn-primary" onClick={handleDownloadPdf}>Download PDF</button>
          <button className="btn btn-red" onClick={() => navigate('/dashboard')}>Done</button>
        </div>
      </div>

      <div className="builder-grid">
        <div className="builder-sidebar">
          {/* Skills */}
          <div className="glass-panel">
            <h2>Available Skills</h2>
            {availableSkills.length === 0 ? <p className="empty-text">No more skills to add.</p> : (
              <div className="available-list">
                {availableSkills.map(s => (
                  <div key={s.id} className="available-item">
                    <span>{s.name}</span>
                    <button onClick={() => handleAddSkill(s.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Experiences */}
          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Experiences</h2>
            {availableExps.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableExps.map(e => (
                  <div key={e.id} className="available-item">
                    <span><strong style={{fontSize:'0.8rem'}}>{e.role}</strong><br/><span style={{fontSize:'0.7rem',color:'#888'}}>{e.company}</span></span>
                    <button onClick={() => handleAddExp(e.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Education */}
          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Education</h2>
            {availableEdus.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableEdus.map(e => (
                  <div key={e.id} className="available-item">
                    <span><strong style={{fontSize:'0.8rem'}}>{e.degree}</strong><br/><span style={{fontSize:'0.7rem',color:'#888'}}>{e.institution}</span></span>
                    <button onClick={() => handleAddEdu(e.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Projects */}
          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Projects</h2>
            {availableProjects.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableProjects.map(p => (
                  <div key={p.id} className="available-item">
                    <span><strong style={{fontSize:'0.8rem'}}>{p.name}</strong></span>
                    <button onClick={() => handleAddProject(p.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Certifications */}
          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Certifications</h2>
            {availableCerts.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableCerts.map(c => (
                  <div key={c.id} className="available-item">
                    <span><strong style={{fontSize:'0.8rem'}}>{c.name}</strong></span>
                    <button onClick={() => handleAddCert(c.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Courses */}
          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Courses</h2>
            {availableCourses.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableCourses.map(c => (
                  <div key={c.id} className="available-item">
                    <span><strong style={{fontSize:'0.8rem'}}>{c.name}</strong></span>
                    <button onClick={() => handleAddCourse(c.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Achievements */}
          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Achievements</h2>
            {availableAchievements.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableAchievements.map(a => (
                  <div key={a.id} className="available-item">
                    <span style={{fontSize:'0.82rem',fontWeight:600}}>{a.title}</span>
                    <button onClick={() => handleAddAchievement(a.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="builder-main">
          <div className={`glass-panel resume-preview ${isPrinting ? 'is-printing' : ''}`} ref={printRef}>
            {/* Header Info */}
            {isPrinting ? (
              <h1 className="resume-title-display">{title || 'Your Name'}</h1>
            ) : (
              <input className="resume-title-input" value={title} onChange={e => setTitle(e.target.value)} onBlur={handleUpdateMetadata} placeholder="Full Name" />
            )}

            {isPrinting ? (
              <div className="resume-designation-display">{designation}</div>
            ) : (
              <input className="resume-designation-input" value={designation} onChange={e => setDesignation(e.target.value)} onBlur={handleUpdateMetadata} placeholder="Designation" />
            )}

            <div className="resume-contact-row">
              <input className="resume-contact-input" value={email} onChange={e => setEmail(e.target.value)} onBlur={handleUpdateMetadata} placeholder="Email" />
              <input className="resume-contact-input" value={phone} onChange={e => setPhone(e.target.value)} onBlur={handleUpdateMetadata} placeholder="Phone" />
              <input className="resume-contact-input" value={location} onChange={e => setLocation(e.target.value)} onBlur={handleUpdateMetadata} placeholder="Location" />
            </div>

            <div className="resume-summary-container">
              <textarea className="resume-summary-input" value={summary} onChange={e => setSummary(e.target.value)} onBlur={handleUpdateMetadata} placeholder="Professional Summary" rows={3} />
              {!isPrinting && <button className="sync-bio-btn ui-only" onClick={handleUseProfileBio}>🔄</button>}
            </div>
            
            <hr className="resume-header-divider" />

            {/* Skills Section */}
            <div 
              className={getSectionClass('skill')}
              onDragOver={(e) => handleDragOver(e, 'skill')}
              onDragLeave={() => setDragOverSection(null)}
              onDrop={(e) => handleDrop(e, 'skill', (resume.skills || []).length)}
            >
              <h3>Skills</h3>
              <div className="skills-list">
                {(resume.skills || []).map((s, idx) => (
                  <span 
                    key={s.id} 
                    className={`skill-tag resume-skill-tag draggable-item ${
                      draggingItem?.item.id === s.id && draggingItem?.type === 'skill' ? 'dragging' : ''
                    } ${
                      dragOverSection === 'skill' && dragOverIndex === idx ? 'drag-over-item' : ''
                    }`}
                    draggable={!isPrinting}
                    onDragStart={(e) => handleDragStart(e, s, 'skill', idx)}
                    onDragOver={(e) => handleDragOver(e, 'skill', idx)}
                    onDrop={(e) => handleDrop(e, 'skill', idx)}
                  >
                    {!isPrinting && (
                      <GripVertical 
                        className="drag-handle-icon drag-handle" 
                        size={14} 
                        onMouseDown={() => setCanDrag(true)}
                        onMouseUp={() => setCanDrag(false)}
                        onMouseLeave={() => setCanDrag(false)}
                      />
                    )}
                    {s.name}
                    <button onClick={() => handleRemoveSkill(s.id)} className="remove-btn ui-only">x</button>
                  </span>
                ))}
              </div>
            </div>

            {/* Experience Section */}
            <div 
              className={getSectionClass('experience')}
              onDragOver={(e) => handleDragOver(e, 'experience')}
              onDragLeave={() => setDragOverSection(null)}
              onDrop={(e) => handleDrop(e, 'experience', (resume.experiences || []).length)}
            >
              <h3>Experience</h3>
              <div className="exp-list">
                {(resume.experiences || []).map((e, idx) => (
                  <div 
                    key={e.id} 
                    className={`resume-exp-item draggable-item ${
                      draggingItem?.item.id === e.id && draggingItem?.type === 'experience' ? 'dragging' : ''
                    } ${
                      dragOverSection === 'experience' && dragOverIndex === idx ? 'drag-over-item' : ''
                    }`}
                    draggable={!isPrinting}
                    onDragStart={(e) => handleDragStart(e, e, 'experience', idx)}
                    onDragOver={(e) => handleDragOver(e, 'experience', idx)}
                    onDrop={(e) => handleDrop(e, 'experience', idx)}
                  >
                    {!isPrinting && (
                      <GripVertical 
                        className="drag-handle-icon-side drag-handle" 
                        size={18} 
                        onMouseDown={() => setCanDrag(true)}
                        onMouseUp={() => setCanDrag(false)}
                        onMouseLeave={() => setCanDrag(false)}
                      />
                    )}
                    <div className="exp-content">
                      <div className="exp-header">
                        <h4>{e.role} <span className="company-text">at {e.company}</span></h4>
                        <button onClick={() => handleRemoveExp(e.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{e.start_date} - {e.end_date}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Education Section */}
            <div 
              className={getSectionClass('education')}
              onDragOver={(e) => handleDragOver(e, 'education')}
              onDragLeave={() => setDragOverSection(null)}
              onDrop={(e) => handleDrop(e, 'education', (resume.educations || []).length)}
            >
              <h3>Education</h3>
              <div className="exp-list">
                {(resume.educations || []).map((e, idx) => (
                  <div 
                    key={e.id} 
                    className={`resume-exp-item draggable-item ${
                      draggingItem?.item.id === e.id && draggingItem?.type === 'education' ? 'dragging' : ''
                    } ${
                      dragOverSection === 'education' && dragOverIndex === idx ? 'drag-over-item' : ''
                    }`}
                    draggable={!isPrinting}
                    onDragStart={(e) => handleDragStart(e, e, 'education', idx)}
                    onDragOver={(e) => handleDragOver(e, 'education', idx)}
                    onDrop={(e) => handleDrop(e, 'education', idx)}
                  >
                    {!isPrinting && (
                      <GripVertical 
                        className="drag-handle-icon-side drag-handle" 
                        size={18} 
                        onMouseDown={() => setCanDrag(true)}
                        onMouseUp={() => setCanDrag(false)}
                        onMouseLeave={() => setCanDrag(false)}
                      />
                    )}
                    <div className="exp-content">
                      <div className="exp-header">
                        <h4>{e.degree} <span className="company-text">at {e.institution}</span></h4>
                        <button onClick={() => handleRemoveEdu(e.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{e.start_date} - {e.end_date}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Projects Section */}
            <div 
              className={getSectionClass('project')}
              onDragOver={(e) => handleDragOver(e, 'project')}
              onDragLeave={() => setDragOverSection(null)}
              onDrop={(e) => handleDrop(e, 'project', (resume.projects || []).length)}
            >
              <h3>Projects</h3>
              <div className="exp-list">
                {(resume.projects || []).map((p, idx) => (
                  <div 
                    key={p.id} 
                    className={`resume-exp-item draggable-item ${
                      draggingItem?.item.id === p.id && draggingItem?.type === 'project' ? 'dragging' : ''
                    } ${
                      dragOverSection === 'project' && dragOverIndex === idx ? 'drag-over-item' : ''
                    }`}
                    draggable={!isPrinting}
                    onDragStart={(e) => handleDragStart(e, p, 'project', idx)}
                    onDragOver={(e) => handleDragOver(e, 'project', idx)}
                    onDrop={(e) => handleDrop(e, 'project', idx)}
                  >
                    {!isPrinting && (
                      <GripVertical 
                        className="drag-handle-icon-side drag-handle" 
                        size={18} 
                        onMouseDown={() => setCanDrag(true)}
                        onMouseUp={() => setCanDrag(false)}
                        onMouseLeave={() => setCanDrag(false)}
                      />
                    )}
                    <div className="exp-content">
                      <div className="exp-header">
                        <h4>{p.name}</h4>
                        <button onClick={() => handleRemoveProject(p.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{formatDate(p.start_date)} - {formatDate(p.end_date)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Certifications Section */}
            <div 
              className={getSectionClass('certification')}
              onDragOver={(e) => handleDragOver(e, 'certification')}
              onDragLeave={() => setDragOverSection(null)}
              onDrop={(e) => handleDrop(e, 'certification', (resume.certifications || []).length)}
            >
              <h3>Certifications</h3>
              <div className="exp-list">
                {(resume.certifications || []).map((c, idx) => (
                  <div 
                    key={c.id} 
                    className={`resume-exp-item draggable-item ${
                      draggingItem?.item.id === c.id && draggingItem?.type === 'certification' ? 'dragging' : ''
                    } ${
                      dragOverSection === 'certification' && dragOverIndex === idx ? 'drag-over-item' : ''
                    }`}
                    draggable={!isPrinting}
                    onDragStart={(e) => handleDragStart(e, c, 'certification', idx)}
                    onDragOver={(e) => handleDragOver(e, 'certification', idx)}
                    onDrop={(e) => handleDrop(e, 'certification', idx)}
                  >
                    {!isPrinting && (
                      <GripVertical 
                        className="drag-handle-icon-side drag-handle" 
                        size={18} 
                        onMouseDown={() => setCanDrag(true)}
                        onMouseUp={() => setCanDrag(false)}
                        onMouseLeave={() => setCanDrag(false)}
                      />
                    )}
                    <div className="exp-content">
                      <div className="exp-header">
                        <h4>{c.name}</h4>
                        <button onClick={() => handleRemoveCert(c.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{c.date}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Courses Section */}
            <div 
              className={getSectionClass('course')}
              onDragOver={(e) => handleDragOver(e, 'course')}
              onDragLeave={() => setDragOverSection(null)}
              onDrop={(e) => handleDrop(e, 'course', (resume.courses || []).length)}
            >
              <h3>Courses</h3>
              <div className="exp-list">
                {(resume.courses || []).map((c, idx) => (
                  <div 
                    key={c.id} 
                    className={`resume-exp-item draggable-item ${
                      draggingItem?.item.id === c.id && draggingItem?.type === 'course' ? 'dragging' : ''
                    } ${
                      dragOverSection === 'course' && dragOverIndex === idx ? 'drag-over-item' : ''
                    }`}
                    draggable={!isPrinting}
                    onDragStart={(e) => handleDragStart(e, c, 'course', idx)}
                    onDragOver={(e) => handleDragOver(e, 'course', idx)}
                    onDrop={(e) => handleDrop(e, 'course', idx)}
                  >
                    {!isPrinting && (
                      <GripVertical 
                        className="drag-handle-icon-side drag-handle" 
                        size={18} 
                        onMouseDown={() => setCanDrag(true)}
                        onMouseUp={() => setCanDrag(false)}
                        onMouseLeave={() => setCanDrag(false)}
                      />
                    )}
                    <div className="exp-content">
                      <div className="exp-header">
                        <h4>{c.name}</h4>
                        <button onClick={() => handleRemoveCourse(c.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{c.date}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Achievements Section */}
            <div 
              className={getSectionClass('achievement')}
              onDragOver={(e) => handleDragOver(e, 'achievement')}
              onDragLeave={() => setDragOverSection(null)}
              onDrop={(e) => handleDrop(e, 'achievement', (resume.achievements || []).length)}
            >
              <h3>Achievements</h3>
              <div className="exp-list">
                {(resume.achievements || []).map((a, idx) => (
                  <div 
                    key={a.id} 
                    className={`resume-exp-item draggable-item ${
                      draggingItem?.item.id === a.id && draggingItem?.type === 'achievement' ? 'dragging' : ''
                    } ${
                      dragOverSection === 'achievement' && dragOverIndex === idx ? 'drag-over-item' : ''
                    }`}
                    draggable={!isPrinting}
                    onDragStart={(e) => handleDragStart(e, a, 'achievement', idx)}
                    onDragOver={(e) => handleDragOver(e, 'achievement', idx)}
                    onDrop={(e) => handleDrop(e, 'achievement', idx)}
                  >
                    {!isPrinting && (
                      <GripVertical 
                        className="drag-handle-icon-side drag-handle" 
                        size={18} 
                        onMouseDown={() => setCanDrag(true)}
                        onMouseUp={() => setCanDrag(false)}
                        onMouseLeave={() => setCanDrag(false)}
                      />
                    )}
                    <div className="exp-content">
                      <div className="exp-header">
                        <h4>{a.title}</h4>
                        <button onClick={() => handleRemoveAchievement(a.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{formatDate(a.date)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeBuilder;
