import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import './Dashboard.css';

const ResumeCard = ({ resume, onDelete, onDuplicate }) => {
  // Tracks the open state of the options menu
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);
  const navigate = useNavigate();

  // Close menu when clicking outside
  useEffect(() => {
    const handler = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const displayName = resume.name || resume.title || 'Untitled Resume';
  // Provides default text for missing summaries
  const displaySummary = resume.summary
    ? resume.summary.substring(0, 80) + (resume.summary.length > 80 ? '...' : '')
    : 'No summary yet';

  return (
    <div
      className="resume-card"
      onClick={() => navigate(`/resume/${resume.id}/edit`)}
    >
      <div className="resume-card-body">
        <div className="resume-card-title">{displayName}</div>
        <div className="resume-card-summary">{displaySummary}</div>
      </div>

      {/* 3-dot menu */}
      <div
        className="resume-card-menu"
        ref={menuRef}
        onClick={e => e.stopPropagation()} // prevent card click
      >
        <button
          className="three-dot-btn"
          onClick={() => setMenuOpen(o => !o)}
          aria-label="Options"
        >
          ⋮
        </button>
        {menuOpen && (
          <div className="dropdown-menu">
            <button onClick={() => { setMenuOpen(false); navigate(`/resume/${resume.id}/edit`); }}>
              ✏️ Edit
            </button>
            <button onClick={() => { setMenuOpen(false); onDuplicate(resume.id); }}>
              📋 Duplicate
            </button>
            <button className="danger" onClick={() => { setMenuOpen(false); onDelete(resume.id); }}>
              🗑️ Delete
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

const Dashboard = () => {
  const [resumes, setResumes] = useState([]);
  const navigate = useNavigate();

  const fetchResumes = async () => {
    try {
      // Fetches all resumes for the current user
      const res = await api.get('/resume');
      setResumes(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => { fetchResumes(); }, []);

  const handleDelete = async (id) => {
    // Confirms deletion intent before removing the resume
    if (!window.confirm('Delete this resume?')) return;
    try {
      await api.delete(`/resume/${id}`);
      fetchResumes();
    } catch (err) { console.error(err); }
  };

  const handleDuplicate = async (id) => {
    try {
      const res = await api.post(`/resume/${id}/duplicate`);
      navigate(`/resume/${res.data.resume_id}/edit`);
    } catch (err) { console.error(err); }
  };

  return (
    <div className="dashboard-container animate-fade-in">
      <div className="dashboard-header">
        <h1 className="text-gradient">My Resumes</h1>
      </div>

      <div className="resumes-grid">
        {/* Create New — always first */}
        <Link to="/resume/new" className="resume-card resume-card-new">
          <div className="resume-card-icon">+</div>
          <div className="resume-card-label">Create New Resume</div>
        </Link>

        {/* Existing resumes */}
        {resumes.map(r => (
          <ResumeCard
            key={r.id}
            resume={r}
            onDelete={handleDelete}
            onDuplicate={handleDuplicate}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
