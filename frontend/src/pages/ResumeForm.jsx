import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const ResumeForm = () => {
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/resume', { title, summary });
      setSuccess(true);
      setTimeout(() => navigate(`/resume/${res.data.resume_id}/edit`), 2000);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container animate-fade-in" style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h1 className="text-gradient">Create New Resume</h1>
      <div className="glass-panel" style={{ padding: '2rem' }}>
        {success && <div style={{background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1.5rem'}}>Resume created successfully! Redirecting...</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Resume Title</label>
            <input 
              type="text" 
              value={title} 
              onChange={e => setTitle(e.target.value)} 
              required 
              placeholder="e.g. Backend Developer Resume"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Professional Summary (Optional)</label>
            <textarea 
              value={summary} 
              onChange={e => setSummary(e.target.value)} 
              placeholder="A brief summary of your professional background..."
              rows={5}
            />
          </div>
          <button type="submit" className="btn btn-primary w-full">Create Resume</button>
        </form>
      </div>
    </div>
  );
};

export default ResumeForm;
