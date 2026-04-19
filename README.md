<div align="center">
  <h1>✨ ResumeBuilder ✨</h1>
  <p><strong>A Premium, Full-Stack AI-Ready Resume Generation Platform</strong></p>
  
  [![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-blue?style=for-the-badge&logo=render)](https://resume-builder-6oxj.onrender.com)
  [![Made with React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![Powered by Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
</div>

---

## 🌟 Overview

**ResumeBuilder** is a state-of-the-art web application designed to help professionals craft elegant, ATS-friendly resumes with zero friction. Built with a robust **Python/Flask backend** and a blazing-fast **React/Vite frontend**, it delivers an executive-grade user experience.

Unlike standard resume builders, this platform emphasizes **Dynamic Design**—featuring glassmorphism, responsive grid layouts, and a seamless dark/light mode toggle—ensuring that building your profile feels as premium as the resume it generates.

---

## 🌐 Live Demo

Check out the live application hosted on Render:  
🔗 **[https://resume-builder-6oxj.onrender.com](https://resume-builder-6oxj.onrender.com)**

---

## 💎 What Makes It Attractive?

- **🎨 Executive-Grade UI/UX:** Built with vanilla CSS emphasizing modern aesthetics—smooth gradients, glassmorphism (`backdrop-filter: blur`), and micro-animations for high user engagement.
- **🌗 Flawless Theme Switching:** A comprehensive Light/Dark mode system that adapts every component, ensuring optimal visibility and a tailored user experience.
- **📄 "White Paper" Document Mode:** Regardless of your global theme (Light or Dark), the live resume preview is locked into a clean, print-ready "Document Mode", guaranteeing what you see is exactly what employers get.
- **⚡ Single Page Application (SPA):** Instant navigation without page reloads, backed by seamless React Router integration and Flask catch-all routing.
- **🔒 Secure Authentication:** 30-day extended JWT sessions keep users logged in seamlessly while maintaining high security.
- **🖨️ One-Click PDF Export:** Instantly generate pixel-perfect PDFs of your resume directly from the browser.

---

## 🛠️ Technology Stack

### **Frontend**
- **React.js & Vite:** For a lightning-fast development experience and optimized production build.
- **Vanilla CSS:** Custom design system without the bloat of external frameworks.
- **React Router DOM:** For client-side routing.
- **Axios:** For robust API communication.
- **Context API:** Managing global State (Authentication & Theme).

### **Backend**
- **Flask:** Lightweight, highly customizable Python web framework.
- **Flask-SQLAlchemy:** ORM for secure database interactions.
- **Flask-JWT-Extended:** Handling authentication and secure sessions.
- **Marshmallow:** Data serialization and validation.
- **PostgreSQL / SQLite:** Environment-adaptive database configuration (SQLite for local dev, PostgreSQL for production).

---

## 🏗️ Features Architecture

1. **Secure Onboarding:** JWT-based user registration and login.
2. **Comprehensive Profile Hub:** Manage Skills, Experiences, Education, Projects, Certifications, Courses, and Achievements.
3. **Dynamic Resume Assembly:** Select which profile items to include in your current resume build.
4. **Real-time Preview:** See your resume update instantly as you select/deselect items.
5. **Unified Deployment:** Configured to serve the React SPA directly from the Flask backend via WSGI (Gunicorn).

---

## 💻 Local Development

Want to run this locally? Here is how:

### 1. Clone the repository
```bash
git clone https://github.com/HITESH-235/resume_builder.git
cd resume_builder
```

### 2. Set up the Backend
```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server (runs on port 5000)
python3 run.py
```

### 3. Set up the Frontend
Open a **new terminal window**:
```bash
cd frontend

# Install Node modules
npm install

# Start the Vite development server
npm run dev
```
*The app will be available at `http://localhost:5173`*

---

## 👨‍💻 Author

**Hitesh Sinha**  
📧 **Email:** codonstream.72@gmail.com  
🐙 **GitHub:** [HITESH-235](https://github.com/HITESH-235)

---
<div align="center">
  <i>Built with ❤️ to make job hunting a little more beautiful.</i>
</div>
