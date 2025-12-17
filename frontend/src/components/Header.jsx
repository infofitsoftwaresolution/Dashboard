import React, { useState, useRef, useEffect } from 'react'
import FilterBar from './FilterBar'
import './Header.css'

function Header({ 
  dateRange, 
  monthRange, 
  selectedPractitioner, 
  selectedProgram, 
  selectedLocation,
  onFilterChange,
  onClearFilters
}) {
  const [showUserMenu, setShowUserMenu] = useState(false)
  const userMenuRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setShowUserMenu(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <header className="app-header">
      <div className="header-left">
        <h1 className="header-page-title">Virtual Scribe</h1>
      </div>
      <div className="header-center">
        <FilterBar
          dateRange={dateRange}
          monthRange={monthRange}
          selectedPractitioner={selectedPractitioner}
          selectedProgram={selectedProgram}
          selectedLocation={selectedLocation}
          onFilterChange={onFilterChange}
        />
      </div>
      <div className="header-right">
        <button className="header-btn clear-filters-btn" onClick={onClearFilters}>
          Clear Filters
        </button>
        <button className="header-btn saved-filters-btn">
          Saved Filters
        </button>
        <div className="user-profile-dropdown" ref={userMenuRef}>
          <button 
            className="user-profile-btn"
            onClick={() => setShowUserMenu(!showUserMenu)}
          >
            <div className="user-avatar">
              <span>👤</span>
            </div>
            <span className="user-name">User</span>
            <span className="dropdown-arrow">{showUserMenu ? '▲' : '▼'}</span>
          </button>
          {showUserMenu && (
            <div className="user-menu">
              <div className="user-menu-item">Profile</div>
              <div className="user-menu-item">Settings</div>
              <div className="user-menu-divider"></div>
              <div className="user-menu-item">Logout</div>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header

