import React, { useState, useRef, useEffect } from 'react'
import './FilterDropdown.css'

function FilterDropdown({ label, options, selectedValue, onSelect, isOpen, onToggle }) {
  const dropdownRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        onToggle(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
      return () => document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen, onToggle])

  const handleSelect = (value) => {
    onSelect(value)
    onToggle(false)
  }

  const handleClear = () => {
    onSelect(null)
    onToggle(false)
  }

  return (
    <div className="filter-dropdown-container" ref={dropdownRef}>
      <div className="filter-dropdown-header" onClick={() => onToggle(!isOpen)}>
        <span>{label}</span>
        <span className="dropdown-arrow">{isOpen ? '▲' : '▼'}</span>
      </div>
      {isOpen && (
        <div className="filter-dropdown-menu">
          <div className="filter-dropdown-options">
            {options && options.length > 0 ? (
              <>
                <div className="filter-option" onClick={handleClear}>
                  <span className={selectedValue === null ? 'selected' : ''}>All {label}s</span>
                </div>
                {options.map((option, index) => (
                  <div
                    key={index}
                    className={`filter-option ${selectedValue === option ? 'selected' : ''}`}
                    onClick={() => handleSelect(option)}
                  >
                    {option}
                  </div>
                ))}
              </>
            ) : (
              <div className="filter-option disabled">No options available</div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default FilterDropdown

