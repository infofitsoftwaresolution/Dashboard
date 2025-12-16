import React from 'react'
import './Header.css'

function Header() {
  return (
    <header className="app-header">
      <div className="header-left">
        <span className="version">v1.2512.28</span>
      </div>
      <div className="header-right">
        <span className="header-title">Bells Support myAvatar Dev</span>
        <div className="header-actions">
          <button className="header-icon-btn">
            <span>🔔</span>
          </button>
          <button className="header-icon-btn">
            <span>❓</span>
          </button>
          <div className="user-avatar">
            <span>👤</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header

