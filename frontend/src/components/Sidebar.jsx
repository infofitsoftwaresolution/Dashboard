import React from 'react'
import './Sidebar.css'

function Sidebar({ activeSection, onSectionChange, onSettings, onEdit }) {
  const reports = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'audit', label: 'Audit Trail Summary', icon: '📋' },
    { id: 'patient-access', label: 'Patient Access Logs', icon: '👤' },
    { id: 'patient-service', label: 'Patient Service Usage', icon: '🏥' },
    { id: 'recommendation', label: 'Similarity Recommendations', icon: '💡' },
    { id: 'delivery', label: 'Report Schedules', icon: '📅' },
    { id: 'signed', label: 'Finalized Notes', icon: '✅' },
    { id: 'practitioner', label: 'Practitioner Activity', icon: '👨‍⚕️' },
    { id: 'sync', label: 'Session Sync Issues', icon: '🔄' },
    { id: 'unsigned', label: 'Pending Notes', icon: '📝' }
  ]

  return (
    <div className="sidebar">
      <div className="sidebar-section">
        <h3 className="sidebar-heading">REPORTS</h3>
        <ul className="sidebar-menu">
          {reports.map((report) => (
            <li key={report.id}>
              <button
                className={`sidebar-item ${activeSection === report.id ? 'active' : ''}`}
                onClick={() => onSectionChange(report.id)}
              >
                <span className="sidebar-icon">{report.icon}</span>
                <span className="sidebar-label">{report.label}</span>
                {activeSection === report.id && report.id === 'dashboard' && (
                  <span className="active-indicator"></span>
                )}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default Sidebar

