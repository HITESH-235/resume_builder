import React, { useContext } from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ThemeContext } from '../context/ThemeContext';
import './Layout.css';

const Layout = () => {
  const { user, logout } = useContext(AuthContext);
  const { theme, toggleTheme } = useContext(ThemeContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clears the session and redirects to login
    logout();
    navigate('/login');
  };

  return (
    <div className="layout">
      <header className="glass-panel nav-header">
        <div className="container nav-container">
          <Link to="/" className="brand" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--primary)' }}>
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <span className="text-gradient">ResumeBuilder</span>
          </Link>
          <nav className="nav-links">
            <button 
              className="theme-toggle" 
              onClick={toggleTheme} 
              title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            >
              {theme === 'light' ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="18.36" x2="5.64" y2="16.94"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
              )}
            </button>
            {/* Renders authenticated or unauthenticated navigation links */}
            {user ? (
              <>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/profile">Profile</Link>
                <button className="btn btn-outline" onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn btn-outline">Login</Link>
                <Link to="/register" className="btn btn-primary">Sign Up</Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="container main-content animate-fade-in">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
