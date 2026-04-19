import React from 'react';
import { Link } from 'react-router-dom';
import './Landing.css';

const Landing = () => {
  return (
    <div className="landing-container animate-fade-in">
      <div className="hero-section glass-panel">
        <h1 className="hero-title text-gradient">Build Your Future, One Resume at a Time</h1>
        <p className="hero-subtitle">
          Create professional, dynamic resumes that stand out. Manage your skills, experience, and education in one centralized profile and perfectly tailor your resume to every job application.
        </p>
        <div className="hero-cta">
          <Link to="/register" className="btn btn-primary btn-large">Get Started Now</Link>
          <Link to="/login" className="btn btn-outline btn-large">Log In</Link>
        </div>
      </div>

      <div className="features-grid">
        <div className="feature-card glass-panel">
          <div className="feature-icon">✨</div>
          <h3>Dynamic Generation</h3>
          <p>Instantly generate perfectly formatted resumes based on your master profile data.</p>
        </div>
        <div className="feature-card glass-panel">
          <div className="feature-icon">🎯</div>
          <h3>Tailored Applications</h3>
          <p>Pick and choose which skills, experiences, and education to highlight for specific job listings.</p>
        </div>
        <div className="feature-card glass-panel">
          <div className="feature-icon">🚀</div>
          <h3>Modern Design</h3>
          <p>Your resume is presented with an industry-standard layout that is built to get past ATS systems.</p>
        </div>
      </div>
    </div>
  );
};

export default Landing;
