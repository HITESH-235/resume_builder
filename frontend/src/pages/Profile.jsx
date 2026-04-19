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
  
  // New entry states
  const [newSkill, setNewSkill] = useState('');
  const [newExp, setNewExp] = useState({ company: '', role: '', start_date: '', end_date: '' });
  const [newEdu, setNewEdu] = useState({ institution: '', degree: '', start_date: '', end_date: '', description: '' });
  const [newProject, setNewProject] = useState({ name: '', role: '', description: '', link: '', start_date: '', end_date: '' });
  const [newCert, setNewCert] = useState({ name: '', issuer: '', url: '', date: '' });
  const [newCourse, setNewCourse] = useState({ name: '', institution: '', date: '' });
  const [newAchievement, setNewAchievement] = useState({ title: '', description: '', date: '' });

  useEffect(() => {
    // Fetches profile data on component mount
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const fullRes = await api.get('/profile/full');
      const data = fullRes.data.data;
      setProfile(data.profile || {});
      setExperiences(data.experiences || []);
      setEducations(data.educations || []);
      setSkills(data.skills || []);
      setProjects(data.projects || []);
      setCertifications(data.certifications || []);
      setCourses(data.courses || []);
      setAchievements(data.achievements || []);
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
    try {
      await api.delete(`/profile/skills/${id}`);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddExp = async (e) => {
    e.preventDefault();
    try {
      const expData = { ...newExp };
      // Ensures end_date is null for current experiences
      if (!expData.end_date) expData.end_date = null;
      await api.post('/profile/experience', expData);
      setNewExp({ company: '', role: '', start_date: '', end_date: '' });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteExp = async (id) => {
    try {
      await api.delete(`/profile/experience/${id}`);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddEdu = async (e) => {
    e.preventDefault();
    try {
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
    try {
      await api.delete(`/profile/education/${id}`);
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddProject = async (e) => {
    e.preventDefault();
    try {
      const pData = { ...newProject };
      if (!pData.end_date) pData.end_date = null;
      await api.post('/profile/project', pData);
      setNewProject({ name: '', role: '', description: '', link: '', start_date: '', end_date: '' });
      fetchData();
    } catch (err) { console.error(err); }
  };

  const handleDeleteProject = async (id) => {
    try { await api.delete(`/profile/project/${id}`); fetchData(); } catch (err) { console.error(err); }
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
    try { await api.delete(`/profile/certification/${id}`); fetchData(); } catch (err) { console.error(err); }
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
    try { await api.delete(`/profile/course/${id}`); fetchData(); } catch (err) { console.error(err); }
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
    try { await api.delete(`/profile/achievement/${id}`); fetchData(); } catch (err) { console.error(err); }
  };

  return (
    <div className="profile-container animate-fade-in">
      <h1 className="text-gradient">Your Profile</h1>
      
      <div className="profile-grid">

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
                <span key={s.id} className="skill-tag">
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
              <input type="text" placeholder="Course Name" value={newCourse.name} onChange={e => setNewCourse({...newCourse, name: e.target.value})} required />
              <input type="text" placeholder="Institution" value={newCourse.institution} onChange={e => setNewCourse({...newCourse, institution: e.target.value})} required />
              <input type="date" value={newCourse.date} onChange={e => setNewCourse({...newCourse, date: e.target.value})} required />
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
                  <div className="exp-dates">{c.institution} · {new Date(c.date).toLocaleDateString()}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel profile-card card-achievement">
          <h2>Achievements</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddAchievement} className="vertical-form">
              <input type="text" placeholder="Achievement Title" value={newAchievement.title} onChange={e => setNewAchievement({...newAchievement, title: e.target.value})} required />
              <input type="date" value={newAchievement.date} onChange={e => setNewAchievement({...newAchievement, date: e.target.value})} required />
              <textarea placeholder="Description (Optional)" value={newAchievement.description} onChange={e => setNewAchievement({...newAchievement, description: e.target.value})} rows={2} />
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
                  <div className="exp-dates">{new Date(a.date).toLocaleDateString()}</div>
                  {a.description && <p style={{margin:'0.25rem 0 0',fontSize:'0.78rem',color:'#555'}}>{a.description}</p>}
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
              <input type="text" placeholder="Company" value={newExp.company} onChange={e => setNewExp({...newExp, company: e.target.value})} required />
              <input type="text" placeholder="Role" value={newExp.role} onChange={e => setNewExp({...newExp, role: e.target.value})} required />
              <div className="date-group">
                <input type="date" value={newExp.start_date} onChange={e => setNewExp({...newExp, start_date: e.target.value})} required />
                <input type="date" value={newExp.end_date} onChange={e => setNewExp({...newExp, end_date: e.target.value})} />
              </div>
              <button type="submit" className="btn btn-primary submit-btn">Add Experience</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list">
              {experiences.map(e => (
                <div key={e.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{e.role} <span style={{fontWeight:'normal',color:'var(--text-muted)'}}>@ {e.company}</span></h3>
                    <button onClick={() => handleDeleteExp(e.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates">{new Date(e.start_date).toLocaleDateString()} – {e.end_date ? new Date(e.end_date).toLocaleDateString() : 'Present'}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel profile-card card-cert">
          <h2>Certifications</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddCert} className="exp-form">
              <input type="text" placeholder="Certification Name" value={newCert.name} onChange={e => setNewCert({...newCert, name: e.target.value})} required />
              <input type="text" placeholder="Issuer" value={newCert.issuer} onChange={e => setNewCert({...newCert, issuer: e.target.value})} required />
              <input type="url" placeholder="URL (Optional)" value={newCert.url} onChange={e => setNewCert({...newCert, url: e.target.value})} />
              <input type="date" value={newCert.date} onChange={e => setNewCert({...newCert, date: e.target.value})} required />
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
                  <div className="exp-dates">{c.issuer} · {new Date(c.date).toLocaleDateString()}</div>
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
              <input type="text" placeholder="Institution" value={newEdu.institution} onChange={e => setNewEdu({...newEdu, institution: e.target.value})} required />
              <input type="text" placeholder="Degree / Field of Study" value={newEdu.degree} onChange={e => setNewEdu({...newEdu, degree: e.target.value})} required />
              <div className="date-group">
                <input type="date" value={newEdu.start_date} onChange={e => setNewEdu({...newEdu, start_date: e.target.value})} required />
                <input type="date" value={newEdu.end_date} onChange={e => setNewEdu({...newEdu, end_date: e.target.value})} />
              </div>
              <textarea placeholder="Description / Coursework (Optional)" value={newEdu.description} onChange={e => setNewEdu({...newEdu, description: e.target.value})} rows={2} />
              <button type="submit" className="btn btn-primary submit-btn">Add Education</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list">
              {educations.map(e => (
                <div key={e.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{e.degree} <span style={{fontWeight:'normal',color:'var(--text-muted)'}}>@ {e.institution}</span></h3>
                    <button onClick={() => handleDeleteEdu(e.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates">{new Date(e.start_date).toLocaleDateString()} – {e.end_date ? new Date(e.end_date).toLocaleDateString() : 'Present'}</div>
                  {e.description && <p style={{margin:'0.25rem 0 0',fontSize:'0.78rem',color:'#555'}}>{e.description}</p>}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="glass-panel profile-card profile-card-full">
          <h2>Projects</h2>
          <div className="profile-form-area">
            <form onSubmit={handleAddProject} className="vertical-form">
              <input type="text" placeholder="Project Name" value={newProject.name} onChange={e => setNewProject({...newProject, name: e.target.value})} required />
              <input type="text" placeholder="Your Role (Optional)" value={newProject.role} onChange={e => setNewProject({...newProject, role: e.target.value})} />
              <input type="url" placeholder="Project Link (Optional)" value={newProject.link} onChange={e => setNewProject({...newProject, link: e.target.value})} />
              <div className="date-group">
                <input type="date" value={newProject.start_date} onChange={e => setNewProject({...newProject, start_date: e.target.value})} required />
                <input type="date" value={newProject.end_date} onChange={e => setNewProject({...newProject, end_date: e.target.value})} />
              </div>
              <textarea placeholder="Description" value={newProject.description} onChange={e => setNewProject({...newProject, description: e.target.value})} rows={2} />
              <button type="submit" className="btn btn-primary submit-btn">Add Project</button>
            </form>
          </div>
          <div className="profile-list-area">
            <div className="exp-list">
              {projects.map(p => (
                <div key={p.id} className="exp-item">
                  <div className="exp-header">
                    <h3>{p.name}{p.role && <span style={{fontWeight:'normal',color:'var(--text-muted)'}}> – {p.role}</span>}</h3>
                    <button onClick={() => handleDeleteProject(p.id)} className="btn-danger btn-small">✕</button>
                  </div>
                  <div className="exp-dates">{new Date(p.start_date).toLocaleDateString()} – {p.end_date ? new Date(p.end_date).toLocaleDateString() : 'Present'}</div>
                  {p.link && <div style={{fontSize:'0.74rem'}}><a href={p.link} target="_blank" rel="noreferrer">{p.link}</a></div>}
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Profile;
