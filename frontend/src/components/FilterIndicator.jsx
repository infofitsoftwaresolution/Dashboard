import React from 'react'
import './FilterIndicator.css'

function FilterIndicator({ dateRange, monthRange, practitioner, program, location, recordCount, onClear }) {
  const hasFilters = dateRange || monthRange || practitioner || program || location

  if (!hasFilters) return null

  return (
    <div className="filter-indicator">
      <div className="filter-indicator-header">
        <span className="filter-indicator-title">
          <span className="filter-icon">🔍</span>
          Active Filters
          {recordCount !== null && (
            <span className="record-count">({recordCount} records)</span>
          )}
        </span>
        {onClear && (
          <button className="clear-all-filters-btn" onClick={() => onClear('all')}>
            Clear All
          </button>
        )}
      </div>
      <div className="filter-tags">
        {dateRange && (
          <span className="filter-tag">
            Date: {new Date(dateRange.start).toLocaleDateString()} - {new Date(dateRange.end).toLocaleDateString()}
            {onClear && <button className="filter-tag-remove" onClick={(e) => { e.stopPropagation(); onClear('date'); }}>×</button>}
          </span>
        )}
        {monthRange && (
          <span className="filter-tag">
            Month: {monthRange.start} - {monthRange.end}
            {onClear && <button className="filter-tag-remove" onClick={(e) => { e.stopPropagation(); onClear('month'); }}>×</button>}
          </span>
        )}
        {practitioner && (
          <span className="filter-tag">
            Practitioner: {practitioner}
            {onClear && <button className="filter-tag-remove" onClick={(e) => { e.stopPropagation(); onClear('practitioner'); }}>×</button>}
          </span>
        )}
        {program && (
          <span className="filter-tag">
            Program: {program}
            {onClear && <button className="filter-tag-remove" onClick={(e) => { e.stopPropagation(); onClear('program'); }}>×</button>}
          </span>
        )}
        {location && (
          <span className="filter-tag">
            Location: {location}
            {onClear && <button className="filter-tag-remove" onClick={(e) => { e.stopPropagation(); onClear('location'); }}>×</button>}
          </span>
        )}
      </div>
    </div>
  )
}

export default FilterIndicator

