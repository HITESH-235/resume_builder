import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import './Profile.css';

const Profile = () => {
  // Manages state for all profile sections
  const [profile, setProfile] = useState({});
  const [experiences, setExperiences] = useState([]);
  const [educations, setEducations] = useState([]);
  const [skills, setSkills] = useState([]);
  const [projects, setProjects] = useState([]);
  const [certifications, setCertifications] = useState([]);
  const [courses, setCourses] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [customItems, setCustomItems] = useState([]);

  // New entry states
  const [newSkill, setNewSkill] = useState('');
  const [newExp, setNewExp] = useState({ company: '', role: '', start_date: '', end_date: '' });
  const [newEdu, setNewEdu] = useState({ institution: '', degree: '', start_date: '', end_date: '', description: '' });
  const [newProject, setNewProject] = useState({ name: '', role: '', description: '', link: '', start_date: '', end_date: '' });
  const [newCert, setNewCert] = useState({ name: '', issuer: '', url: '', date: '' });
  const [newCourse, setNewCourse] = useState({ name: '', institution: '', date: '' });
  const [newAchievement, setNewAchievement] = useState({ title: '', description: '', date: '' });
  const [newCustomItem, setNewCustomItem] = useState({ title: '', subtitle: '', description: '', start_date: '', end_date: '' });
  const [showNewTitleInput, setShowNewTitleInput] = useState(false);
  const [selectedTitle, setSelectedTitle] = useState('');

  const [personalInfo, setPersonalInfo] = useState({ full_name: '', bio: '' });

  useEffect(() => {
    // Fetches profile data on component mount
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await api.get('/profile/custom-item');
      const items = res.data.custom_items || [];
      setCustomItems(items);
      const uniqueTitles = [...new Set(items.map(item => item.title))];
      if (uniqueTitles.length > 0) {
        setSelectedTitle(uniqueTitles[0]);
        setNewCustomItem(prev => ({ ...prev, title: uniqueTitles[0] }));
      } else {
        setShowNewTitleInput(true);
        setSelectedTitle('new');
      }
      const fullRes = await api.get('/profile');
      const data = fullRes.data.data;
      setProfile(data.profile || {});
      setExperiences(data.experiences || []);
      setEducations(data.educations || []);
      setSkills(data.skills || []);
      setProjects(data.projects || []);
      setCertifications(data.certifications || []);
      setCourses(data.courses || []);
      setAchievements(data.achievements || []);
      setCustomItems(data.custom_items || []);
      setPersonalInfo({
        full_name: data.profile?.full_name || '',
        bio: data.profile?.bio || ''
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddSkill = async (e) => {
    e.preventDefault();
    if (!newSkill) return; // Prevents submission of empty skills
    try {
      await api.post('/profile/skills', { skills: [newSkill] });
      setNewSkill('');
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteSkill = async (id) => {
    // Optimistic Update: Remove from UI immediately
    setSkills(prev => prev.filter(s => s.id !== id));
    try {
      await api.delete(`/profile/skills/${id}`);
      // No need to fetchData() unless we want to sync with server-side auto-generated fields
    } catch (err) {
      console.error(err);
      fetchData(); // Rollback on error
    }
  };

  const handleAddExp = async (e) => {
    e.preventDefault();
    try {
      if (newExp.end_date && new Date(newExp.start_date) > new Date(newExp.end_date)) {
        alert("Start date cannot be after the end date.");
        return;
      }
      const expData = { ...newExp };
      if (!expData.end_date) expData.end_date = null;
      await api.post('/profile/experience', expData);
      setNewExp({ company: '', role: '', start_date: '', end_date: '' });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteExp = async (id) => {
    setExperiences(prev => prev.filter(e => e.id !== id));
    try {
      await api.delete(`/profile/experience/${id}`);
    } catch (err) {
      console.error(err);
      fetchData();
    }
  };

  const handleAddEdu = async (e) => {
    e.preventDefault();
    try {
      if (newEdu.end_date && new Date(newEdu.start_date) > new Date(newEdu.end_date)) {
        alert("Start date cannot be after the end date.");
        return;
      }
      const eduData = { ...newEdu };
      if (!eduData.end_date) eduData.end_date = null;
      await api.post('/profile/education', eduData);
      setNewEdu({ institution: '', degree: '', start_date: '', end_date: '', description: '' });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteEdu = async (id) => {
    setEducations(prev => prev.filter(e => e.id !== id));
    try {
      await api.delete(`/profile/education/${id}`);
    } catch (err) {
      console.error(err);
      fetchData();
    }
  };

  const handleAddProject = async (e) => {
    e.preventDefault();
    try {
      if (newProject.end_date && new Date(newProject.start_date) > new Date(newProject.end_date)) {
        alert("Start date cannot be after the end date.");
        return;
      }
      const pData = { ...newProject };
      if (!pData.end_date) pData.end_date = null;
      await api.post('/profile/project', pData);
      setNewProject({ name: '', role: '', description: '', link: '', start_date: '', end_date: '' });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleDeleteProject = async (id) => {
    setProjects(prev => prev.filter(p => p.id !== id));
    try { await api.delete(`/profile/project/${id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddCert = async (e) => {
    e.preventDefault();
    try {
      await api.post('/profile/certification', newCert);
      setNewCert({ name: '', issuer: '', url: '', date: '' });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleDeleteCert = async (id) => {
    setCertifications(prev => prev.filter(c => c.id !== id));
    try { await api.delete(`/profile/certification/${id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddCourse = async (e) => {
    e.preventDefault();
    try {
      await api.post('/profile/course', newCourse);
      setNewCourse({ name: '', institution: '', date: '' });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleDeleteCourse = async (id) => {
    setCourses(prev => prev.filter(c => c.id !== id));
    try { await api.delete(`/profile/course/${id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddAchievement = async (e) => {
    e.preventDefault();
    try {
      await api.post('/profile/achievement', newAchievement);
      setNewAchievement({ title: '', description: '', date: '' });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleDeleteAchievement = async (id) => {
    setAchievements(prev => prev.filter(a => a.id !== id));
    try { await api.delete(`/profile/achievement/${id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleAddCustomItem = async (e) => {
    e.preventDefault();
    try {
      if (newCustomItem.end_date && new Date(newCustomItem.start_date) > new Date(newCustomItem.end_date)) {
        alert("Start date cannot be after the end date.");
        return;
      }
      await api.post('/profile/custom-item', newCustomItem);
      setNewCustomItem({ title: '', subtitle: '', start_date: '', end_date: '', description: '' });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleDeleteCustomItem = async (id) => {
    setCustomItems(prev => prev.filter(i => i.id !== id));
    try { await api.delete(`/profile/custom-item/${id}`); } catch (err) { console.error(err); fetchData(); }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      await api.put('/profile', personalInfo);
      alert('Profile updated successfully!');
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="profile-container animate-fade-in">
      <h1 className="text-gradient">Your Profile</h1>

      <div className="profile-grid">
        {/* ── Row 0: Personal Info (Full Width) ── */}
        <div className="glass-panel profile-card profile-card-full personal-info-card">
          <h2>Personal Information</h2>
          <form onSubmit={handleUpdateProfile} className="personal-info-form">
            <div className="info-inputs">              <div className="input-group">
                <label>Full Name</label>
                <input 
                  type="text" 
                  placeholder="e.g. Hitesh Sinha" 
                  value={personalInfo.full_name} 
                  onChange={e => setPersonalInfo({ ...personalInfo, full_name: e.target.value })} 
                />
              </div>
              <div className="input-group">
                <label>Professional Bio</label>
                <textarea 
                  placeholder="Tell us about yourself..." 
                  value={personalInfo.bio} 
                  onChange={e => setPersonalInfo({ ...personalInfo, bio: e.target.value })} 
                  rows={3}
                />
              </div>
            </div>
            <button type="submit" className="btn btn-primary save-btn">Save Profile Changes</button>
          </form>
        </div>

        {/* ── Row 1: Small Sections (2 columns each) ── */}
        <div className="glass-panel profile-card card-skill">
          <h2>Skills</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddSkill} className="add-form">
              <input type="text" placeholder="e.g. React, Python" value={newSkill} onChange={e => setNewSkill(e.target.value)} />
              <button type="submit" className="btn btn-primary">Add</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="skills-list">
              {skills.map(s => (
                <span key={s.id} className="skill-tag text-red">
                  {s.name}
                  <button onClick={() => handleDeleteSkill(s.id)} className="btn-danger btn-small" style={{ display: 'inline-flex', marginLeft: '0.5rem', width: '16px', height: '16px', fontSize: '10px', verticalAlign: 'middle' }}>✕</button>
                </span>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel profile-card card-course">
          <h2>Courses</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddCourse} className="exp-form">
              <input type="text" placeholder="Course Name" value={newCourse.name} onChange={e => setNewCourse({ ...newCourse, name: e.target.value })} required />
              <input type="text" placeholder="Institution" value={newCourse.institution} onChange={e => setNewCourse({ ...newCourse, institution: e.target.value })} required />
              <input type="date" value={newCourse.date} onChange={e => setNewCourse({ ...newCourse, date: e.target.value })} required />
              <button type="submit" className="btn btn-primary submit-btn">Add Course</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list">
              {courses.map(c => (
                <div key={c.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{c.name}</h3>
                    <button onClick={() => handleDeleteCourse(c.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates text-red">{c.institution} · {new Date(c.date).toLocaleDateString()}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel profile-card card-achievement">
          <h2>Achievements</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddAchievement} className="vertical-form">
              <input type="text" placeholder="Achievement Title" value={newAchievement.title} onChange={e => setNewAchievement({ ...newAchievement, title: e.target.value })} required />
              <input type="date" value={newAchievement.date} onChange={e => setNewAchievement({ ...newAchievement, date: e.target.value })} required />
              <textarea placeholder="Description (Optional)" value={newAchievement.description} onChange={e => setNewAchievement({ ...newAchievement, description: e.target.value })} rows={2} />
              <button type="submit" className="btn btn-primary submit-btn">Add Achievement</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list">
              {achievements.map(a => (
                <div key={a.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{a.title}</h3>
                    <button onClick={() => handleDeleteAchievement(a.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates text-red">{new Date(a.date).toLocaleDateString()}</div>
                  {a.description && <p style={{ margin: '0.25rem 0 0', fontSize: '0.78rem', color: '#555' }}>{a.description}</p>}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── Row 2: Medium Sections (3 columns each) ── */}
        <div className="glass-panel profile-card card-exp">
          <h2>Experience</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddExp} className="exp-form">
              <input type="text" placeholder="Company" value={newExp.company} onChange={e => setNewExp({ ...newExp, company: e.target.value })} required />
              <input type="text" placeholder="Role" value={newExp.role} onChange={e => setNewExp({ ...newExp, role: e.target.value })} required />
              <div className="date-group">
                <input type="date" value={newExp.start_date} onChange={e => setNewExp({ ...newExp, start_date: e.target.value })} required />
                <input type="date" value={newExp.end_date} onChange={e => setNewExp({ ...newExp, end_date: e.target.value })} />
              </div>
              <button type="submit" className="btn btn-primary submit-btn">Add Experience</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list">
              {experiences.map(e => (
                <div key={e.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{e.role} <span className="text-red" style={{ fontWeight: 'normal' }}>@ {e.company}</span></h3>
                    <button onClick={() => handleDeleteExp(e.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates text-red">{new Date(e.start_date).toLocaleDateString()} – {e.end_date ? new Date(e.end_date).toLocaleDateString() : 'Present'}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel profile-card card-cert">
          <h2>Certifications</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddCert} className="exp-form">
              <input type="text" placeholder="Certification Name" value={newCert.name} onChange={e => setNewCert({ ...newCert, name: e.target.value })} required />
              <input type="text" placeholder="Issuer" value={newCert.issuer} onChange={e => setNewCert({ ...newCert, issuer: e.target.value })} required />
              <input type="url" placeholder="URL (Optional)" value={newCert.url} onChange={e => setNewCert({ ...newCert, url: e.target.value })} />
              <input type="date" value={newCert.date} onChange={e => setNewCert({ ...newCert, date: e.target.value })} required />
              <button type="submit" className="btn btn-primary submit-btn">Add Certification</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list">
              {certifications.map(c => (
                <div key={c.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{c.name}</h3>
                    <button onClick={() => handleDeleteCert(c.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates text-red">{c.issuer} · {new Date(c.date).toLocaleDateString()}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── Row 3: Full Width Sections (6 columns) ── */}
        <div className="glass-panel profile-card profile-card-full">
          <h2>Education</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddEdu} className="vertical-form">
              <input type="text" placeholder="Institution" value={newEdu.institution} onChange={e => setNewEdu({ ...newEdu, institution: e.target.value })} required />
              <input type="text" placeholder="Degree / Field of Study" value={newEdu.degree} onChange={e => setNewEdu({ ...newEdu, degree: e.target.value })} required />
              <div className="date-group">
                <input type="date" value={newEdu.start_date} onChange={e => setNewEdu({ ...newEdu, start_date: e.target.value })} required />
                <input type="date" value={newEdu.end_date} onChange={e => setNewEdu({ ...newEdu, end_date: e.target.value })} />
              </div>
              <textarea placeholder="Description / Coursework (Optional)" value={newEdu.description} onChange={e => setNewEdu({ ...newEdu, description: e.target.value })} rows={2} />
              <button type="submit" className="btn btn-primary submit-btn">Add Education</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list custom-grid">
              {educations.map(e => (
                <div key={e.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{e.degree} <span className="text-red" style={{ fontWeight: 'normal' }}>@ {e.institution}</span></h3>
                    <button onClick={() => handleDeleteEdu(e.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates">{new Date(e.start_date).toLocaleDateString()} – {e.end_date ? new Date(e.end_date).toLocaleDateString() : 'Present'}</div>
                  {e.description && <p style={{ margin: '0.25rem 0 0', fontSize: '0.78rem', color: '#555' }}>{e.description}</p>}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel profile-card profile-card-full">
          <h2>Projects</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddProject} className="vertical-form">
              <input type="text" placeholder="Project Name" value={newProject.name} onChange={e => setNewProject({ ...newProject, name: e.target.value })} required />
              <input type="text" placeholder="Your Role (Optional)" value={newProject.role} onChange={e => setNewProject({ ...newProject, role: e.target.value })} />
              <input type="url" placeholder="Project Link (Optional)" value={newProject.link} onChange={e => setNewProject({ ...newProject, link: e.target.value })} />
              <div className="date-group">
                <input type="date" value={newProject.start_date} onChange={e => setNewProject({ ...newProject, start_date: e.target.value })} required />
                <input type="date" value={newProject.end_date} onChange={e => setNewProject({ ...newProject, end_date: e.target.value })} />
              </div>
              <textarea placeholder="Description" value={newProject.description} onChange={e => setNewProject({ ...newProject, description: e.target.value })} rows={2} />
              <button type="submit" className="btn btn-primary submit-btn">Add Project</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list custom-grid">
              {projects.map(p => (
                <div key={p.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{p.name}{p.role && <span className="text-red" style={{ fontWeight: 'normal' }}> – {p.role}</span>}</h3>
                    <button onClick={() => handleDeleteProject(p.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates text-red">{new Date(p.start_date).toLocaleDateString()} – {p.end_date ? new Date(p.end_date).toLocaleDateString() : 'Present'}</div>
                  {p.link && <div style={{ fontSize: '0.74rem' }}><a href={p.link} target="_blank" rel="noreferrer">{p.link}</a></div>}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel profile-card profile-card-full card-custom">
          <h2>Custom Item Sections (Volunteer, Hobbies, etc.)</h2>
          <div className="profile-form-area">
            <p className="section-hint" style={{marginBottom: '1.25rem'}}>Each unique <strong>Title</strong> will create a new section/table on your resume.</p>
            <form onSubmit={handleAddCustomItem} className="vertical-form">
              <div className="date-group">
                <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: '0.5rem'}}>
                  <select 
                    value={selectedTitle} 
                    onChange={e => {
                      const val = e.target.value;
                      setSelectedTitle(val);
                      if (val === 'new') {
                        setShowNewTitleInput(true);
                        setNewCustomItem({ ...newCustomItem, title: '' });
                      } else {
                        setShowNewTitleInput(false);
                        setNewCustomItem({ ...newCustomItem, title: val });
                      }
                    }}
                    className="dropdown-select"
                  >
                    {[...new Set(customItems.map(i => i.title))].map(t => (
                      <option key={t} value={t}>{t}</option>
                    ))}
                    <option value="new">+ Add New Category...</option>
                  </select>
                  {showNewTitleInput && (
                    <input 
                      type="text" 
                      placeholder="Category Name (e.g. Volunteer Work)" 
                      value={newCustomItem.title} 
                      onChange={e => setNewCustomItem({ ...newCustomItem, title: e.target.value })} 
                      required 
                      autoFocus
                    />
                  )}
                </div>
                <input type="text" placeholder="Entry Subtitle (e.g. Org Name)" value={newCustomItem.subtitle} onChange={e => setNewCustomItem({ ...newCustomItem, subtitle: e.target.value })} />
              </div>
              <div className="date-group">
                <input type="date" value={newCustomItem.start_date} onChange={e => setNewCustomItem({ ...newCustomItem, start_date: e.target.value })} />
                <input type="date" value={newCustomItem.end_date} onChange={e => setNewCustomItem({ ...newCustomItem, end_date: e.target.value })} />
              </div>
              <textarea placeholder="Description" value={newCustomItem.description} onChange={e => setNewCustomItem({ ...newCustomItem, description: e.target.value })} rows={2} />
              <button type="submit" className="btn btn-primary submit-btn">Add to Section</button>
            </form>
          </div>
          <div className="profile-list-area">
            {Object.entries(customItems.reduce((acc, item) => {
              if (!acc[item.title]) acc[item.title] = [];
              acc[item.title].push(item);
              return acc;
            }, {})).map(([title, items]) => (
              <div key={title} className="custom-category-group">
                <h3 className="category-header">{title}</h3>
                <div className="exp-list custom-grid">
                  {items.map(item => (
                    <div key={item.id} className="exp-item">
                      <div className="exp-header">
                        <h4>{item.subtitle || '(No Subtitle)'}</h4>
                        <button onClick={() => handleDeleteCustomItem(item.id)} className="btn-danger btn-small">✕</button>
                      </div>
                      {(item.start_date || item.end_date) && (
                        <div className="exp-dates text-red">
                          {item.start_date ? new Date(item.start_date).toLocaleDateString() : ''} 
                          {item.start_date && item.end_date ? ' – ' : ''}
                          {item.end_date ? new Date(item.end_date).toLocaleDateString() : ''}
                        </div>
                      )}
                      {item.description && <p style={{ margin: '0.25rem 0 0', fontSize: '0.78rem', color: '#555' }}>{item.description}</p>}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

export default Profile;
