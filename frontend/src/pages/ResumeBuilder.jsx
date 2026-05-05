import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import html2pdf from 'html2pdf.js';
import { 
  GripVertical, 
  FileText, 
  User,
  Plus, 
  Trash2, 
  Grid,
  Mail,
  Phone,
  MapPin,
  ChevronDown,
  ChevronUp,
  Columns,
  Globe,
  Link as LinkIcon
} from 'lucide-react';
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
  const [website, setWebsite] = useState('');
  const [websiteLabel, setWebsiteLabel] = useState('');
  const [profileData, setProfileData] = useState({ 
    experiences: [], 
    educations: [], 
    skills: [], 
    projects: [], 
    certifications: [], 
    courses: [], 
    achievements: [],
    custom_items: [] 
  });
  const [loading, setLoading] = useState(true);
  const [isPrinting, setIsPrinting] = useState(false);
  const [profileBio, setProfileBio] = useState('');
  const [activeTab, setActiveTab] = useState('Layout'); // 'Layout' or 'Content'
  
  // Drag and drop state for items
  const [draggingItem, setDraggingItem] = useState(null);
  const [dragOverSection, setDragOverSection] = useState(null);
  const [dragOverIndex, setDragOverIndex] = useState(null);
  const [canDrag, setCanDrag] = useState(false);
  
  // Drag and drop state for layout sections
  const [draggingSection, setDraggingSection] = useState(null);
  const [tempSplit, setTempSplit] = useState(50);

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
      const r = resRes.data;
      setName(r.name || r.title || '');
      setTitle(r.title || '');
      setSummary(r.summary || '');
      setDesignation(r.designation || '');
      setEmail(r.email || '');
      setPhone(r.phone || '');
      setLocation(r.location || '');
      setWebsite(r.website || '');
      setWebsiteLabel(r.website_label || '');
      setTempSplit(r.layout_config?.column_split || 50);
      
      const p = profRes.data.data;
      setProfileData({
        experiences: p.experiences || [],
        educations: p.educations || [],
        skills: p.skills || [],
        projects: p.projects || [],
        certifications: p.certifications || [],
        courses: p.courses || [],
        achievements: p.achievements || [],
        custom_items: p.custom_items || []
      });
      setProfileBio(p.profile?.bio || '');
    } catch (err) {
      console.error(err);
      if (err.response?.status === 404) navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const parts = dateStr.split(' ')[0].split('-');
    return parts.length >= 2 ? `${parts[1]}-${parts[0]}` : dateStr;
  };

  // --- Handlers ---
  const handleUpdateMetadata = async () => {
    try {
      await api.put(`/resume/${id}`, { 
        title, name, summary, designation, email, phone, location, website, website_label: websiteLabel 
      });
    } catch (err) { console.error(err); }
  };

  const handleAddSection = (type) => {
    // Deep copy to ensure nested arrays are new references
    const newConfig = resume.layout_config ? JSON.parse(JSON.stringify(resume.layout_config)) : { rows: [{ columns: [{ sections: [] }] }] };
    
    let added = false;
    if (newConfig.rows && newConfig.rows.length > 0) {
      for (const row of newConfig.rows) {
        for (const col of row.columns) {
          if (!col.sections.includes(type)) {
            col.sections.push(type);
            added = true;
            break;
          }
        }
        if (added) break;
      }
    }

    if (!added) {
      if (!newConfig.rows) newConfig.rows = [];
      newConfig.rows.push({
        columns: [{ sections: [type] }]
      });
    }

    // Sync active_sections as well
    const activeSections = [];
    newConfig.rows.forEach(r => r.columns.forEach(c => c.sections.forEach(s => activeSections.push(s))));
    
    handleUpdateLayout(newConfig, activeSections);
  };

  const handleUpdateLayout = async (newConfig, activeSections) => {
    try {
      const payload = { layout_config: newConfig };
      if (activeSections) payload.active_sections = activeSections;
      
      await api.put(`/resume/${id}`, payload);
      setResume(prev => ({ ...prev, layout_config: newConfig, active_sections: activeSections || prev.active_sections }));
    } catch (err) { console.error(err); }
  };

  const handleAddGeneric = async (type, payload) => {
    try {
      // Optimistically update UI
      const listKey = type === 'custom_item' ? 'custom_items' : type + 's';
      if (resume[listKey]) {
         // We don't have the full item yet, but we can set a loading state if needed
      }
      
      const res = await api.post(`/resume/${id}/${type.replace('_', '-')}`, payload);
      if (res.status === 201 || res.status === 200) {
        await fetchData();
      }
    } catch (err) { 
      console.error(err);
      alert(err.response?.data?.error || "Failed to add item");
    }
  };

  const handleRemoveGeneric = async (type, itemId) => {
    try {
      await api.delete(`/resume/${id}/${type.replace('_', '-')}/${itemId}`);
      await fetchData();
    } catch (err) { 
      console.error(err);
      alert(err.response?.data?.error || "Failed to remove item");
    }
  };

  // --- Layout Manager Helpers ---
  const addRow = () => {
    const newLayout = resume.layout_config ? JSON.parse(JSON.stringify(resume.layout_config)) : { rows: [], column_split: 50 };
    if (!newLayout.rows) newLayout.rows = [];
    newLayout.rows.push({ columns: [{ sections: [] }] });
    handleUpdateLayout(newLayout);
  };

  const removeRow = (idx) => {
    if (!resume.layout_config) return;
    const newLayout = JSON.parse(JSON.stringify(resume.layout_config));
    newLayout.rows.splice(idx, 1);
    handleUpdateLayout(newLayout);
  };

  const toggleRowColumns = (rowIdx) => {
    if (!resume.layout_config) return;
    const newLayout = JSON.parse(JSON.stringify(resume.layout_config));
    const row = newLayout.rows[rowIdx];
    if (row.columns.length < 2) {
      // Split
      row.columns.push({ sections: [] });
    } else {
      // Merge: move sections from second column to first column
      const secondColSections = row.columns[1].sections || [];
      row.columns[0].sections = [...row.columns[0].sections, ...secondColSections];
      row.columns.splice(1, 1);
    }
    handleUpdateLayout(newLayout);
  };

  const removeColumn = (rowIdx, colIdx) => {
    if (!resume.layout_config) return;
    const newLayout = JSON.parse(JSON.stringify(resume.layout_config));
    newLayout.rows[rowIdx].columns.splice(colIdx, 1);
    if (newLayout.rows[rowIdx].columns.length === 0) {
      newLayout.rows.splice(rowIdx, 1);
    }
    handleUpdateLayout(newLayout);
  };

  const removeSectionFromLayout = (rowIdx, colIdx, secIdx) => {
    if (!resume.layout_config) return;
    const newLayout = JSON.parse(JSON.stringify(resume.layout_config));
    newLayout.rows[rowIdx].columns[colIdx].sections.splice(secIdx, 1);
    handleUpdateLayout(newLayout);
  };

  // --- Drag and Drop for Items ---
  const handleDragStart = (e, item, type, index) => {
    if (!canDrag) { e.preventDefault(); return; }
    setDraggingItem({ item, type, index });
    // Don't reset canDrag here, it will be reset on dragEnd or mouseUp
  };

  const handleDragEnd = () => {
    setDraggingItem(null);
    setDragOverSection(null);
    setDragOverIndex(null);
    setCanDrag(false);
  };

  const handleDragOver = (e, sectionType, index = null) => {
    e.preventDefault();
    if (dragOverSection !== sectionType) setDragOverSection(sectionType);
    if (index !== null && dragOverIndex !== index) setDragOverIndex(index);
  };

  const handleDrop = async (e, type, targetIndex, customTitle = null) => {
    e.preventDefault();
    if (!draggingItem || draggingItem.type !== type) {
      setDragOverSection(null);
      setDragOverIndex(null);
      return;
    }

    const sourceIndex = draggingItem.index;
    if (sourceIndex === targetIndex) {
      setDragOverSection(null);
      setDragOverIndex(null);
      return;
    }

    try {
      const endpointMap = {
        experience: 'experience/order',
        skill: 'skill/order',
        education: 'education/order',
        project: 'project/reorder',
        certification: 'certification/reorder',
        course: 'course/reorder',
        achievement: 'achievement/reorder',
        custom_item: 'custom-item/order'
      };

      const pluralMap = {
        experience: 'experiences',
        skill: 'skills',
        education: 'educations',
        project: 'projects',
        certification: 'certifications',
        course: 'courses',
        achievement: 'achievements'
      };

      const plural = pluralMap[type];
      let orderedIds;

      if (type === 'custom_item' && customTitle) {
        const allItems = [...(resume.custom_items || [])];
        const otherItems = allItems.filter(i => i.title !== customTitle);
        const sectionItems = allItems.filter(i => i.title === customTitle);
        
        const [movedItem] = sectionItems.splice(sourceIndex, 1);
        sectionItems.splice(targetIndex, 0, movedItem);
        
        // Combine back to maintain global order if needed, 
        // but backend usually just needs the IDs for the affected section.
        orderedIds = sectionItems.map(item => item.id);
      } else {
        const items = [...(resume[plural] || [])];
        const [movedItem] = items.splice(sourceIndex, 1);
        items.splice(targetIndex, 0, movedItem);
        orderedIds = items.map(item => item.id);
      }

      await api.put(`/resume/${id}/${endpointMap[type]}`, { ordered_ids: orderedIds });
      fetchData();
    } catch (err) {
      console.error("Reorder failed:", err);
    }
    setDragOverSection(null);
    setDragOverIndex(null);
  };

  // --- Drag and Drop for Sections (Layout) ---
  const handleSectionDragStart = (e, sectionName, sourceRow = null, sourceCol = null, sourceIdx = null) => {
    setDraggingSection({ name: sectionName, r: sourceRow, c: sourceCol, i: sourceIdx });
  };

  const handleSectionDrop = (targetRowIdx, targetColIdx, targetSecIdx = null) => {
    if (!draggingSection) return;
    const newLayout = resume.layout_config ? JSON.parse(JSON.stringify(resume.layout_config)) : { rows: [{ columns: [{ sections: [] }, { sections: [] }] }], column_split: 50 };
    
    // 1. Remove from source position if it was already in layout
    if (draggingSection.r !== null) {
      newLayout.rows[draggingSection.r].columns[draggingSection.c].sections.splice(draggingSection.i, 1);
    } else {
      // If it's a new section from the bottom lists, remove any existing instance (move instead of copy)
      newLayout.rows.forEach(r => r.columns.forEach(c => {
        c.sections = (c.sections || []).filter(s => s !== draggingSection.name);
      }));
    }
    
    // 2. Add to target position
    const targetCol = newLayout.rows[targetRowIdx].columns[targetColIdx];
    if (targetSecIdx !== null) {
      targetCol.sections.splice(targetSecIdx, 0, draggingSection.name);
    } else {
      targetCol.sections.push(draggingSection.name);
    }
    
    // 3. Re-calculate active sections
    const activeSections = [];
    newLayout.rows.forEach(r => r.columns.forEach(c => c.sections.forEach(s => activeSections.push(s))));
    
    handleUpdateLayout(newLayout, activeSections);
    setDraggingSection(null);
  };

  const handleDownloadPdf = () => {
    const element = printRef.current;
    setIsPrinting(true);
    setTimeout(() => {
      const opt = {
        margin: 10,
        filename: `${name || 'Resume'}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };
      html2pdf().from(element).set(opt).save().then(() => setIsPrinting(false));
    }, 500);
  };

  if (loading) return <div className="loading-screen">Loading...</div>;
  if (!resume) return <div className="error-screen">Resume not found.</div>;

  const handleImportBio = () => {
    setSummary(profileBio);
    handleUpdateMetadata();
  };

  const renderSection = (type) => {
    // Check if it's a dynamic custom section (prefixed with 'custom:')
    if (type.startsWith('custom:')) {
      const sectionTitle = type.split('custom:')[1];
      const items = (resume.custom_items || []).filter(item => item.title === sectionTitle);
      if (items.length === 0) return null;

      return (
        <div key={type} className={`resume-section ${dragOverSection === 'custom_item' ? 'valid-drop' : ''}`} onDragOver={(e) => handleDragOver(e, 'custom_item')} onDrop={(e) => handleDrop(e, 'custom_item', items.length, sectionTitle)}>
          <h3>{sectionTitle}</h3>
          {items.map((item, idx) => {
            const details = getItemDetails(item, 'custom_item');
            return (
              <div key={item.id} className={`resume-item draggable-item ${draggingItem?.type === 'custom_item' && draggingItem?.item.id === item.id ? 'dragging' : ''} ${dragOverSection === 'custom_item' && dragOverIndex === idx ? 'drag-over-item' : ''}`} draggable onDragStart={(e) => handleDragStart(e, item, 'custom_item', idx)} onDragEnd={handleDragEnd} onDragOver={(e) => handleDragOver(e, 'custom_item', idx)} onDrop={(e) => { e.stopPropagation(); handleDrop(e, 'custom_item', idx, sectionTitle); }}>
                <div className="item-header">
                  <div style={{display:'flex', alignItems:'center', gap:'4px', width:'100%'}}>
                    {!isPrinting && <GripVertical className="drag-handle-icon" size={16} onMouseDown={() => setCanDrag(true)} />}
                    <h4 className="resume-item-title-row">
                      <span className="title-text">{details.title}</span>
                      {details.subtitle && (
                        <>
                          <span className="title-separator"> | </span>
                          <span className="subtitle-text">{details.subtitle}</span>
                        </>
                      )}
                    </h4>
                  </div>
                </div>
                {(item.start_date || item.end_date) && <div className="date-text">{formatDate(item.start_date)} - {formatDate(item.end_date)}</div>}
                {item.description && <p>{item.description}</p>}
              </div>
            );
          })}
        </div>
      );
    }

    const data = resume[type] || [];
    if (data.length === 0 && type !== 'summary') return null;

    switch(type) {
      case 'summary':
        return (
          <div className="resume-section" key="summary">
            <div className="resume-section-header">
              <h3>Professional Summary</h3>
              {!isPrinting && (
                <button className="import-bio-btn" onClick={handleImportBio} title="Import bio from your profile">
                  <FileText size={12} /> Use Bio
                </button>
              )}
            </div>
            <div className="summary-wrapper" data-replicated-value={summary}>
              <textarea 
                className="resume-summary-input" 
                value={summary} 
                onChange={e => setSummary(e.target.value)} 
                onBlur={handleUpdateMetadata} 
                rows={1}
                placeholder="Write your professional summary here..."
              />
            </div>
          </div>
        );
      case 'skills':
        return (
          <div key="skills" className={`resume-section ${dragOverSection === 'skill' ? 'valid-drop' : ''}`} onDragOver={(e) => handleDragOver(e, 'skill')} onDrop={(e) => handleDrop(e, 'skill', data.length)}>
            <h3>Skills</h3>
            <div className="skills-list">
              {data.map((s, idx) => (
                <span key={s.id} className={`resume-skill-tag draggable-item ${draggingItem?.type === 'skill' && draggingItem?.item.id === s.id ? 'dragging' : ''} ${dragOverSection === 'skill' && dragOverIndex === idx ? 'drag-over-item' : ''}`} draggable onDragStart={(e) => handleDragStart(e, s, 'skill', idx)} onDragEnd={handleDragEnd} onDragOver={(e) => handleDragOver(e, 'skill', idx)} onDrop={(e) => { e.stopPropagation(); handleDrop(e, 'skill', idx); }}>
                  {!isPrinting && <GripVertical className="drag-handle-icon" size={14} onMouseDown={() => setCanDrag(true)} />}
                  {s.name}
                </span>
              ))}
            </div>
          </div>
        );
      default:
        const singular = type.slice(0, -1);
        return (
          <div key={type} className={`resume-section ${dragOverSection === singular ? 'valid-drop' : ''}`} onDragOver={(e) => handleDragOver(e, singular)} onDrop={(e) => handleDrop(e, singular, data.length)}>
            <h3>{type.replace('_', ' ')}</h3>
            {data.map((item, idx) => {
              const details = getItemDetails(item, singular);
              return (
                <div key={item.id} className={`resume-item draggable-item ${draggingItem?.type === singular && draggingItem?.item.id === item.id ? 'dragging' : ''} ${dragOverSection === singular && dragOverIndex === idx ? 'drag-over-item' : ''}`} draggable onDragStart={(e) => handleDragStart(e, item, singular, idx)} onDragEnd={handleDragEnd} onDragOver={(e) => handleDragOver(e, singular, idx)} onDrop={(e) => { e.stopPropagation(); handleDrop(e, singular, idx); }}>
                  <div className="item-header">
                    <div style={{display:'flex', alignItems:'center', gap:'4px', width:'100%'}}>
                      {!isPrinting && <GripVertical className="drag-handle-icon" size={16} onMouseDown={() => setCanDrag(true)} />}
                      <h4 className="resume-item-title-row">
                        <span className="title-text">{details.title}</span>
                        {details.subtitle && (
                          <>
                            <span className="title-separator"> | </span>
                            <span className="subtitle-text">{details.subtitle}</span>
                          </>
                        )}
                      </h4>
                    </div>
                  </div>
                  <div className="date-text">{formatDate(item.start_date || item.date)} {item.end_date ? `- ${formatDate(item.end_date)}` : ''}</div>
                  {item.description && <p>{item.description}</p>}
                </div>
              );
            })}
          </div>
        );
    }
  };

  // Get all unique custom titles from both profile and resume
  const customTitles = Array.from(new Set([
    ...(profileData.custom_items || []).map(i => i.title),
    ...(resume.custom_items || []).map(i => i.title)
  ])).filter(Boolean);

  const getItemDetails = (item, type) => {
    switch(type) {
      case 'education': return { title: item.degree || 'Degree', subtitle: item.institution || 'Institution' };
      case 'experience': return { title: item.role || 'Role', subtitle: item.company || 'Company' };
      case 'project': return { title: item.name || 'Project Name', subtitle: item.role || '' };
      case 'skill': return { title: item.name, subtitle: '' };
      case 'custom_item': return { title: item.subtitle || item.title, subtitle: '' }; /* Removed repeating title */
      case 'certification': return { title: item.name, subtitle: item.issuer };
      case 'course': return { title: item.name, subtitle: item.institution };
      case 'achievement': return { title: item.title, subtitle: '' };
      default: return { title: item.title || item.name || item.role || 'Unnamed Item', subtitle: '' };
    }
  };

  const activeSections = [];
  resume.layout_config?.rows?.forEach(r => r.columns?.forEach(c => c.sections?.forEach(s => activeSections.push(s))));
  const activeSectionSet = new Set(activeSections);

  return (
    <div className={`builder-container ${isPrinting ? 'is-printing' : ''}`}>
      <div className="builder-header ui-only">
        <div className="builder-heading-group">
          <span className="builder-heading-label">Resume Name</span>
          <input className="builder-heading-input" value={name} onChange={e => setName(e.target.value)} onBlur={handleUpdateMetadata} />
        </div>
        <div className="header-actions">
          <button className="btn btn-primary" onClick={handleDownloadPdf}>Download PDF</button>
          <button className="btn btn-red" onClick={() => navigate('/dashboard')}>Done</button>
        </div>
      </div>

      <div className="builder-grid">
        <div className="builder-sidebar ui-only">
          <div className="builder-tabs">
            <button className={`tab-btn ${activeTab === 'Layout' ? 'active' : ''}`} onClick={() => setActiveTab('Layout')}>
              <Grid size={14} /> Layout Grid
            </button>
            <button className={`tab-btn ${activeTab === 'Content' ? 'active' : ''}`} onClick={() => setActiveTab('Content')}>
              <FileText size={14} /> Content
            </button>
          </div>

          <div className="sidebar-scroll">
            {activeTab === 'Content' ? (
              <>
                <div className="glass-panel" style={{marginBottom:'1.5rem'}}>
                  <h2 style={{marginBottom:'1rem'}}>Personal Details</h2>
                  <div className="sidebar-contact-inputs">
                    <div className="input-with-icon" title="Designation">
                      <User size={14} />
                      <input placeholder="Designation (e.g. Software Engineer)" value={designation} onChange={e => setDesignation(e.target.value)} onBlur={handleUpdateMetadata} />
                    </div>
                    <div className="input-with-icon" title="Email">
                      <Mail size={14} />
                      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} onBlur={handleUpdateMetadata} />
                    </div>
                    <div className="input-with-icon" title="Phone">
                      <Phone size={14} />
                      <input placeholder="Phone" value={phone} onChange={e => setPhone(e.target.value)} onBlur={handleUpdateMetadata} />
                    </div>
                    <div className="input-with-icon" title="Location">
                      <MapPin size={14} />
                      <input placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} onBlur={handleUpdateMetadata} />
                    </div>
                    <div className="input-with-icon" title="Website/Link URL">
                      <Globe size={14} />
                      <input placeholder="Website URL (e.g. https://...)" value={website} onChange={e => setWebsite(e.target.value)} onBlur={handleUpdateMetadata} />
                    </div>
                  </div>
                </div>

                <div className="glass-panel">
                  <div className="resume-section-header" style={{marginBottom:'1rem'}}>
                    <h2 style={{margin:0}}>Summary</h2>
                  </div>
                  
                  <h2 style={{marginTop:'2rem'}}>Sections Content</h2>
                  <p className="sidebar-hint" style={{marginBottom:'1.5rem'}}>Add or remove items from active layout sections.</p>
                  
                  {[
                    { label: 'Skills', type: 'skill', profile: profileData.skills, added: resume.skills, active: activeSectionSet.has('skills') },
                    { label: 'Experience', type: 'experience', profile: profileData.experiences, added: resume.experiences, active: activeSectionSet.has('experiences') },
                    { label: 'Education', type: 'education', profile: profileData.educations, added: resume.educations, active: activeSectionSet.has('educations') },
                    { label: 'Projects', type: 'project', profile: profileData.projects, added: resume.projects, active: activeSectionSet.has('projects') },
                    { label: 'Certifications', type: 'certification', profile: profileData.certifications, added: resume.certifications, active: activeSectionSet.has('certifications') },
                    { label: 'Courses', type: 'course', profile: profileData.courses, added: resume.courses, active: activeSectionSet.has('courses') },
                    { label: 'Achievements', type: 'achievement', profile: profileData.achievements, added: resume.achievements, active: activeSectionSet.has('achievements') }
                  ].map(sec => sec.active && (
                    <div key={sec.type} className="section-picker">
                      <h3>{sec.label}</h3>
                      <div className="available-list">
                        {sec.profile.map(item => {
                          const alreadyIn = (sec.added || []).find(ai => ai.id === item.id);
                          const details = getItemDetails(item, sec.type);
                          return (
                            <div key={item.id} className={`sidebar-item-row ${alreadyIn ? 'added' : ''}`}>
                              {alreadyIn ? (
                                <button className="btn-small btn-danger" title="Remove from Resume" onClick={() => handleRemoveGeneric(sec.type, item.id)}>✕</button>
                              ) : (
                                <button className="btn-small btn-primary" title="Add to Resume" onClick={() => handleAddGeneric(sec.type, { [`${sec.type}_id`]: item.id, order: 1 })}>+</button>
                              )}
                              <div className="sidebar-item-info">
                                <div className="sidebar-item-title">{details.title}</div>
                                {details.subtitle && <div className="sidebar-item-subtitle">{details.subtitle}</div>}
                              </div>
                            </div>
                          );
                        })}
                        {sec.profile.length === 0 && <p className="empty-hint">No items in Profile</p>}
                      </div>
                    </div>
                  ))}

                  {customTitles.map(title => {
                    const isActive = activeSectionSet.has(`custom:${title}`);
                    if (!isActive) return null;

                    const itemsInProfile = (profileData.custom_items || []).filter(i => i.title === title);

                    return (
                      <div key={title} className="section-picker">
                        <h3>{title}</h3>
                        <div className="available-list">
                          {itemsInProfile.map(item => {
                            const alreadyIn = (resume.custom_items || []).find(ai => ai.id === item.id);
                            const details = getItemDetails(item, 'custom_item');
                            return (
                              <div key={item.id} className={`sidebar-item-row ${alreadyIn ? 'added' : ''}`}>
                                {alreadyIn ? (
                                  <button className="btn-small btn-danger" title="Remove" onClick={() => handleRemoveGeneric('custom_item', item.id)}>✕</button>
                                ) : (
                                  <button className="btn-small btn-primary" title="Add" onClick={() => handleAddGeneric('custom_item', { custom_item_id: item.id, order: 1 })}>+</button>
                                )}
                                <div className="sidebar-item-info">
                                  <div className="sidebar-item-title">{details.title}</div>
                                  {details.subtitle && <div className="sidebar-item-subtitle">{details.subtitle}</div>}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </>
            ) : (
              <div className="glass-panel">
                <h2>Layout Grid Editor</h2>
                
                <div className="split-slider-container">
                  <div style={{display:'flex', justifyContent:'space-between', marginBottom:'0.5rem'}}>
                    <span style={{fontSize:'0.8rem', opacity:0.7}}>Left Column Width</span>
                    <span style={{fontSize:'0.8rem', fontWeight:'bold', color:'var(--primary)'}}>{tempSplit}%</span>
                  </div>
                  <input type="range" className="split-slider" min="20" max="80" value={tempSplit} 
                    onChange={e => setTempSplit(parseInt(e.target.value))} 
                    onMouseUp={() => {
                      const newLayout = { ...resume.layout_config, column_split: tempSplit };
                      handleUpdateLayout(newLayout);
                    }}
                  />
                </div>

                <div className="layout-grid-editor">
                  <div className="layout-header-chip">
                    <User size={16} /> <span>Personal Header</span>
                  </div>
                  
                  {resume.layout_config?.rows?.map((row, rIdx) => (
                    <div key={rIdx} className="layout-row-editor">
                      <div className="row-cols">
                        {row.columns.map((col, cIdx) => (
                          <div key={cIdx} className="col-editor" onDragOver={e => e.preventDefault()} onDrop={() => handleSectionDrop(rIdx, cIdx)}>
                            {col.sections.map((s, sIdx) => (
                              <div 
                                key={sIdx} 
                                className="section-chip-card" 
                                draggable 
                                onDragStart={e => handleSectionDragStart(e, s, rIdx, cIdx, sIdx)}
                                onDragOver={e => e.preventDefault()}
                                onDrop={e => { e.stopPropagation(); handleSectionDrop(rIdx, cIdx, sIdx); }}
                              >
                                <GripVertical size={12} className="chip-handle" />
                                <span className="chip-content">{s.startsWith('custom:') ? s.split('custom:')[1] : s.replace('_', ' ')}</span>
                                <Trash2 size={12} style={{marginLeft:'auto', cursor:'pointer', opacity:0.6}} onClick={() => removeSectionFromLayout(rIdx, cIdx, sIdx)} />
                              </div>
                            ))}
                            {col.sections.length === 0 && <div className="empty-slot"></div>}
                          </div>
                        ))}
                      </div>
                      <div className="row-actions">
                        <button className="row-action-btn" onClick={() => toggleRowColumns(rIdx)} title={row.columns.length > 1 ? "Merge Columns" : "Split Row"}>
                          {row.columns.length > 1 ? <Grid size={12} /> : <Columns size={12} />}
                        </button>
                        <button className="row-action-btn delete" onClick={() => removeRow(rIdx)}><Trash2 size={12} /></button>
                      </div>
                    </div>
                  ))}
                  
                  <button className="btn btn-outline btn-full mt-2" onClick={addRow}><Plus size={14} /> Add Row</button>
                  
                  <div className="mt-4">
                    <h3>Standard Sections</h3>
                    <div className="section-adder-grid">
                      {['summary', 'skills', 'experiences', 'educations', 'projects', 'certifications', 'courses', 'achievements'].map(s => (
                        <div key={s} className="section-chip-card" draggable onDragStart={e => handleSectionDragStart(e, s)} onClick={() => handleAddSection(s)}>
                          <Plus size={12} /> <span style={{textTransform:'capitalize'}}>{s.replace('_', ' ')}</span>
                        </div>
                      ))}
                    </div>

                    <h3 className="mt-3">Custom Sections (from Profile)</h3>
                    <div className="section-adder-grid">
                      {customTitles.map(title => (
                        <div key={title} className="section-chip-card" draggable onDragStart={e => handleSectionDragStart(e, `custom:${title}`)} onClick={() => handleAddSection(`custom:${title}`)}>
                          <Plus size={12} /> <span>{title}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="builder-main">
          <div className={`resume-preview ${isPrinting ? 'is-printing' : ''}`} ref={printRef}>
            <div className="resume-header">
              <input className="resume-title-input" value={title} onChange={e => setTitle(e.target.value)} onBlur={handleUpdateMetadata} />
              {designation && <div className="resume-designation-display">{designation}</div>}
              <div className="resume-contact-row">
                {email && <span className="resume-contact-display"><Mail size={12} /> {email}</span>}
                {phone && <span className="resume-contact-display"><Phone size={12} /> {phone}</span>}
                {location && <span className="resume-contact-display"><MapPin size={12} /> {location}</span>}
                {website && (
                  <span className="resume-contact-display">
                    <LinkIcon size={12} style={{marginRight: '4px'}} /> 
                    <a href={website.startsWith('http') ? website : `https://${website}`} target="_blank" rel="noopener noreferrer" style={{color: 'inherit', textDecoration: 'none'}}>
                      {websiteLabel || 'website'}
                    </a>
                  </span>
                )}              </div>
              <hr className="resume-header-divider" />
            </div>
            
            {resume.layout_config?.rows?.map((row, rIdx) => (
              <div key={rIdx} className="resume-row" style={{ 
                display: 'grid', 
                gridTemplateColumns: row.columns?.length > 1 ? `${tempSplit}% 1fr` : '1fr', 
                gap: '40px' 
              }}>
                {row.columns?.map((col, cIdx) => (
                  <div key={cIdx} className="resume-column">
                    {col.sections?.map(s => renderSection(s))}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeBuilder;
