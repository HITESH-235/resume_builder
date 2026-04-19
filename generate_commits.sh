#!/bin/bash

# Navigate to the workspace
cd /home/hit235/projects/flask/resume_builder

# Frontend Commits
git add frontend/src/components/Layout.jsx frontend/src/components/Layout.css
git commit -m "Add layout structure and navigation" || true

git add frontend/src/pages/Login.jsx frontend/src/pages/Register.jsx frontend/src/pages/Auth.css
git commit -m "Add authentication pages" || true

git add frontend/src/pages/Dashboard.jsx frontend/src/pages/Dashboard.css
git commit -m "Add dashboard structure" || true

git add frontend/src/pages/Profile.jsx frontend/src/pages/Profile.css
git commit -m "Add profile section" || true

git add frontend/src/pages/ResumeBuilder.jsx frontend/src/pages/ResumeBuilder.css frontend/src/pages/ResumeForm.jsx
git commit -m "Add resume builder interface" || true

git add frontend/src/pages/Landing.jsx frontend/src/pages/Landing.css
git commit -m "Add landing page" || true

git add frontend/src/api/ frontend/src/context/
git commit -m "Add API and context configuration" || true

git add frontend/src/App.jsx frontend/src/App.css frontend/src/index.css frontend/src/main.jsx
git commit -m "Add main app entry point and global styles" || true

git add frontend/package.json frontend/vite.config.js frontend/index.html
git commit -m "Add frontend project configuration" || true

git add frontend/
git commit -m "Finalize frontend components and UI refinements" || true

# Backend Commits
git add app/resume/
git commit -m "Add backend resume routes and models" || true

git add app/profile/
git commit -m "Add profile API endpoints and service logic" || true

git add app/models/
git commit -m "Add core database models" || true

git commit -am "Add certifications in resume" || true
git commit -am "Add education in resume" || true
git commit -am "Refine full-stack integration and polish code comments" || true

# Catch-all
git add -A
git commit -m "Finalize application build and setup" || true

echo "Done creating simulated commits!"
