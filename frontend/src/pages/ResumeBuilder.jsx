import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import html2pdf from 'html2pdf.js';
import api from '../api/axios';
import './ResumeBuilder.css';

const ResumeBuilder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [resume, setResume] = useState(null);
  const [name, setName] = useState('');       // Dashboard heading / label
  const [title, setTitle] = useState('');     // PDF: Full Name shown on resume
  const [summary, setSummary] = useState('');
  const [designation, setDesignation] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [location, setLocation] = useState('');
  const [profileData, setProfileData] = useState({ experiences: [], educations: [], skills: [], projects: [], certifications: [], courses: [], achievements: [] });
  const [loading, setLoading] = useState(true);
  const [isPrinting, setIsPrinting] = useState(false);
  const printRef = useRef();

  useEffect(() => {
    // Refetches data when the resume ID changes
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const [resRes, profRes] = await Promise.all([
        api.get(`/resume/${id}`),
        api.get('/profile/full')
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
    } catch (err) {
      console.error(err);
      // Redirects to home if the resume is not found
      if (err.response?.status === 404) navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const handleAddSkill = async (skill_id) => {
    try {
      const currentSkills = resume.skills || [];
      // Calculates the order for the new skill
      const order = currentSkills.length > 0 ? Math.max(...currentSkills.map(s => s.order)) + 1 : 1;
      await api.post(`/resume/${id}/skill`, { skill_id, order });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemoveSkill = async (skill_id) => {
    try {
      await api.delete(`/resume/${id}/skill/${skill_id}`);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddExp = async (experience_id) => {
    try {
      const currentExps = resume.experiences || [];
      const order = currentExps.length > 0 ? Math.max(...currentExps.map(e => e.order)) + 1 : 1;
      await api.post(`/resume/${id}/experience`, { experience_id, order });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemoveExp = async (experience_id) => {
    try {
      await api.delete(`/resume/${id}/experience/${experience_id}`);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddEdu = async (education_id) => {
    try {
      const currentEdus = resume.educations || [];
      const order = currentEdus.length > 0 ? Math.max(...currentEdus.map(e => e.order)) + 1 : 1;
      await api.post(`/resume/${id}/education`, { education_id, order });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemoveEdu = async (education_id) => {
    try {
      await api.delete(`/resume/${id}/education/${education_id}`);
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleAddProject = async (project_id) => {
    try {
      const current = resume.projects || [];
      const order = current.length > 0 ? Math.max(...current.map(x => x.order)) + 1 : 1;
      await api.post(`/resume/${id}/project`, { project_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };
  const handleRemoveProject = async (project_id) => {
    try { await api.delete(`/resume/${id}/project/${project_id}`); fetchData(); } catch (err) { console.error(err); }
  };

  const handleAddCert = async (certification_id) => {
    try {
      const current = resume.certifications || [];
      const order = current.length > 0 ? Math.max(...current.map(x => x.order)) + 1 : 1;
      await api.post(`/resume/${id}/certification`, { certification_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };
  const handleRemoveCert = async (certification_id) => {
    try { await api.delete(`/resume/${id}/certification/${certification_id}`); fetchData(); } catch (err) { console.error(err); }
  };

  const handleAddCourse = async (course_id) => {
    try {
      const current = resume.courses || [];
      const order = current.length > 0 ? Math.max(...current.map(x => x.order)) + 1 : 1;
      await api.post(`/resume/${id}/course`, { course_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };
  const handleRemoveCourse = async (course_id) => {
    try { await api.delete(`/resume/${id}/course/${course_id}`); fetchData(); } catch (err) { console.error(err); }
  };

  const handleAddAchievement = async (achievement_id) => {
    try {
      const current = resume.achievements || [];
      const order = current.length > 0 ? Math.max(...current.map(x => x.order)) + 1 : 1;
      await api.post(`/resume/${id}/achievement`, { achievement_id, order });
      fetchData();
    } catch (err) { console.error(err); }
  };
  const handleRemoveAchievement = async (achievement_id) => {
    try { await api.delete(`/resume/${id}/achievement/${achievement_id}`); fetchData(); } catch (err) { console.error(err); }
  };

  const handleUpdateMetadata = async () => {
    if (!title.trim()) return;
    try {
      await api.put(`/resume/${id}`, { title, name, summary, designation, email, phone, location });
    } catch (err) {
      console.error('Failed to update resume metadata', err);
    }
  };

  const handleDownloadPdf = () => {
    const element = printRef.current;
    
    // Set state to render plain text instead of inputs
    setIsPrinting(true);
    
    // Wait for React to re-render
    setTimeout(() => {
      const opt = {
        margin:       15, // Standard professional margins for every page
        filename:     `${(resume.title || 'Resume').replace(/\s+/g, '_')}_Resume.pdf`,
        image:        { type: 'jpeg', quality: 1.0 },
        html2canvas:  { 
          scale: 3,
          useCORS: true, 
          letterRendering: true,
          scrollX: 0,
          scrollY: 0
        },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] }
      };

      html2pdf().from(element).set(opt).save().then(() => {
        setIsPrinting(false);
      });
    }, 100); // Short delay to ensure DOM is updated
  };

  if (loading) return <div>Loading...</div>;
  if (!resume) return <div>Resume not found.</div>;

  // Derives available items to prevent duplicates in the sidebar
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
            placeholder="e.g. Backend Dev Resume, Google Application..."
          />
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn btn-primary" onClick={handleDownloadPdf}>Download PDF</button>
          <button className="btn btn-outline" onClick={() => navigate('/dashboard')}>Done</button>
        </div>
      </div>

      <div className="builder-grid">
        {/* Left Pane: Available Profile Items */}
        <div className="builder-sidebar">
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

          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Projects</h2>
            {availableProjects.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableProjects.map(p => (
                  <div key={p.id} className="available-item">
                    <span><strong style={{fontSize:'0.8rem'}}>{p.name}</strong>{p.role && <><br/><span style={{fontSize:'0.7rem',color:'#888'}}>{p.role}</span></>}</span>
                    <button onClick={() => handleAddProject(p.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Certifications</h2>
            {availableCerts.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableCerts.map(c => (
                  <div key={c.id} className="available-item">
                    <span><strong style={{fontSize:'0.8rem'}}>{c.name}</strong><br/><span style={{fontSize:'0.7rem',color:'#888'}}>{c.issuer}</span></span>
                    <button onClick={() => handleAddCert(c.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="glass-panel" style={{ marginTop: '0.75rem' }}>
            <h2>Available Courses</h2>
            {availableCourses.length === 0 ? <p className="empty-text">None to add.</p> : (
              <div className="available-list">
                {availableCourses.map(c => (
                  <div key={c.id} className="available-item">
                    <span><strong style={{fontSize:'0.8rem'}}>{c.name}</strong><br/><span style={{fontSize:'0.7rem',color:'#888'}}>{c.institution}</span></span>
                    <button onClick={() => handleAddCourse(c.id)} className="btn btn-primary btn-small">+</button>
                  </div>
                ))}
              </div>
            )}
          </div>

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

        {/* Right Pane: Resume Preview */}
        <div className="builder-main" style={{ overflowX: 'auto', paddingBottom: '2rem' }}>
          <div className={`glass-panel resume-preview ${isPrinting ? 'is-printing' : ''}`} ref={printRef}>
            {isPrinting ? (
              <h1 className="resume-title-display">{title || 'Your Name'}</h1>
            ) : (
              <input 
                className="resume-title-input" 
                value={title} 
                onChange={e => setTitle(e.target.value)}
                onBlur={handleUpdateMetadata}
                placeholder="Full Name / Resume Title"
              />
            )}

            {isPrinting ? (
              <div className="resume-designation-display">{designation}</div>
            ) : (
              <input
                className="resume-designation-input"
                value={designation}
                onChange={e => setDesignation(e.target.value)}
                onBlur={handleUpdateMetadata}
                placeholder="Current Designation (e.g. Senior Software Engineer)"
              />
            )}

            <div className="resume-contact-row">
              {isPrinting ? (
                <>
                  {email && <span className="resume-contact-display">{email}</span>}
                  {phone && <span className="resume-contact-display">{phone}</span>}
                  {location && <span className="resume-contact-display">{location}</span>}
                </>
              ) : (
                <>
                  <input
                    className="resume-contact-input"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    onBlur={handleUpdateMetadata}
                    placeholder="Email"
                  />
                  <input
                    className="resume-contact-input"
                    value={phone}
                    onChange={e => setPhone(e.target.value)}
                    onBlur={handleUpdateMetadata}
                    placeholder="Phone"
                  />
                  <input
                    className="resume-contact-input"
                    value={location}
                    onChange={e => setLocation(e.target.value)}
                    onBlur={handleUpdateMetadata}
                    placeholder="Location"
                  />
                </>
              )}
            </div>

            {isPrinting ? (
              <div className="resume-summary-display">{summary}</div>
            ) : (
              <textarea 
                className="resume-summary-input" 
                value={summary} 
                onChange={e => setSummary(e.target.value)}
                onBlur={handleUpdateMetadata}
                placeholder="Professional Summary (Optional)"
                rows={3}
              />
            )}
            <hr className="resume-header-divider" />

            <div className="resume-section">
              <h3>Skills</h3>
              {(resume.skills || []).length === 0 ? <p className="empty-text">No skills added yet.</p> : (
                <div className="skills-list">
                  {resume.skills.map(s => (
                    <span key={s.id} className="skill-tag resume-skill-tag">
                      {s.name}
                      <button onClick={() => handleRemoveSkill(s.id)} className="remove-btn ui-only">x</button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="resume-section">
              <h3>Experience</h3>
              {(resume.experiences || []).length === 0 ? <p className="empty-text">No experiences added yet.</p> : (
                <div className="exp-list">
                  {resume.experiences.map(e => (
                    <div key={e.id} className="resume-exp-item">
                      <div className="exp-header">
                        <h4>{e.role} <span className="company-text">at {e.company}</span></h4>
                        <button onClick={() => handleRemoveExp(e.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{e.start_date} - {e.end_date}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="resume-section">
              <h3>Education</h3>
              {(resume.educations || []).length === 0 ? <p className="empty-text">No education added yet.</p> : (
                <div className="exp-list">
                  {resume.educations.map(e => (
                    <div key={e.id} className="resume-exp-item">
                      <div className="exp-header">
                        <h4>{e.degree} <span className="company-text">at {e.institution}</span></h4>
                        <button onClick={() => handleRemoveEdu(e.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{e.start_date} - {e.end_date}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="resume-section">
              <h3>Projects</h3>
              {(resume.projects || []).length === 0 ? <p className="empty-text">No projects added yet.</p> : (
                <div className="exp-list">
                  {resume.projects.map(p => (
                    <div key={p.id} className="resume-exp-item">
                      <div className="exp-header">
                        <h4>{p.name} {p.role && <span className="company-text">- {p.role}</span>}</h4>
                        <button onClick={() => handleRemoveProject(p.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{p.start_date} - {p.end_date}</div>
                      {p.link && <div><a href={p.link} target="_blank" rel="noreferrer" style={{color: 'var(--primary)', fontSize: '0.85rem'}}>{p.link}</a></div>}
                      {p.description && <p style={{marginTop: '0.5rem', fontSize:'0.9rem', color:'#444'}}>{p.description}</p>}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="resume-section">
              <h3>Certifications</h3>
              {(resume.certifications || []).length === 0 ? <p className="empty-text">No certifications added yet.</p> : (
                <div className="exp-list">
                  {resume.certifications.map(c => (
                    <div key={c.id} className="resume-exp-item">
                      <div className="exp-header">
                        <h4>{c.name} <span className="company-text">by {c.issuer}</span></h4>
                        <button onClick={() => handleRemoveCert(c.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{c.date}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="resume-section">
              <h3>Courses</h3>
              {(resume.courses || []).length === 0 ? <p className="empty-text">No courses added yet.</p> : (
                <div className="exp-list">
                  {resume.courses.map(c => (
                    <div key={c.id} className="resume-exp-item">
                      <div className="exp-header">
                        <h4>{c.name} <span className="company-text">at {c.institution}</span></h4>
                        <button onClick={() => handleRemoveCourse(c.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{c.date}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="resume-section">
              <h3>Achievements</h3>
              {(resume.achievements || []).length === 0 ? <p className="empty-text">No achievements added yet.</p> : (
                <div className="exp-list">
                  {resume.achievements.map(a => (
                    <div key={a.id} className="resume-exp-item">
                      <div className="exp-header">
                        <h4>{a.title}</h4>
                        <button onClick={() => handleRemoveAchievement(a.id)} className="btn-danger btn-small ui-only">✕</button>
                      </div>
                      <div className="date-text">{a.date}</div>
                      {a.description && <p style={{marginTop: '0.5rem', fontSize:'0.9rem', color:'#444'}}>{a.description}</p>}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeBuilder;
