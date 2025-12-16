import React, { useState, useRef, useEffect } from 'react'
import './DateRangePicker.css'

function DateRangePicker({ onDateRangeChange, onMonthRangeChange }) {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedType, setSelectedType] = useState('date') // 'date' or 'month'
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [startMonth, setStartMonth] = useState('')
  const [endMonth, setEndMonth] = useState('')
  const dropdownRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleApply = () => {
    if (selectedType === 'date') {
      if (startDate && endDate) {
        onDateRangeChange({ start: startDate, end: endDate })
      }
    } else {
      if (startMonth && endMonth) {
        // Send "YYYY-MM" format - backend will handle conversion for times endpoint
        onMonthRangeChange({ start: startMonth, end: endMonth })
      }
    }
    setIsOpen(false)
  }

  const handleClear = () => {
    setStartDate('')
    setEndDate('')
    setStartMonth('')
    setEndMonth('')
    // Clear both date and month ranges
    if (onDateRangeChange) {
      onDateRangeChange(null)
    }
    if (onMonthRangeChange) {
      onMonthRangeChange(null)
    }
    setIsOpen(false)
  }

  const getCurrentMonth = () => {
    const now = new Date()
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  }

  const getMonthsList = () => {
    const months = []
    const now = new Date()
    for (let i = 11; i >= 0; i--) {
      const date = new Date(now.getFullYear(), now.getMonth() - i, 1)
      const monthStr = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
      const monthName = date.toLocaleString('default', { month: 'short', year: 'numeric' })
      months.push({ value: monthStr, label: monthName })
    }
    return months
  }

  return (
    <div className="date-range-picker-container" ref={dropdownRef}>
      <button 
        className="filter-icon-btn"
        onClick={() => setIsOpen(!isOpen)}
        title="Filter by date range"
      >
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M2 4H14M2 4V12C2 12.5304 2.21071 13.0391 2.58579 13.4142C2.96086 13.7893 3.46957 14 4 14H12C12.5304 14 13.0391 13.7893 13.4142 13.4142C13.7893 13.0391 14 12.5304 14 12V4M2 4L2 2M14 4V2M6 2V4M10 2V4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
      </button>

      {isOpen && (
        <div className="date-range-dropdown">
          <div className="date-range-header">
            <h4>Filter by Range</h4>
            <button className="close-btn" onClick={() => setIsOpen(false)}>×</button>
          </div>

          <div className="date-range-tabs">
            <button
              className={`tab-btn ${selectedType === 'date' ? 'active' : ''}`}
              onClick={() => setSelectedType('date')}
            >
              Date Range
            </button>
            <button
              className={`tab-btn ${selectedType === 'month' ? 'active' : ''}`}
              onClick={() => setSelectedType('month')}
            >
              Month Range
            </button>
          </div>

          {selectedType === 'date' ? (
            <div className="date-range-content">
              <div className="date-input-group">
                <label>Start Date</label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  max={endDate || undefined}
                />
              </div>
              <div className="date-input-group">
                <label>End Date</label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  min={startDate || undefined}
                />
              </div>
            </div>
          ) : (
            <div className="date-range-content">
              <div className="date-input-group">
                <label>Start Month</label>
                <select
                  value={startMonth}
                  onChange={(e) => setStartMonth(e.target.value)}
                >
                  <option value="">Select month</option>
                  {getMonthsList().map((month) => (
                    <option key={month.value} value={month.value}>
                      {month.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className="date-input-group">
                <label>End Month</label>
                <select
                  value={endMonth}
                  onChange={(e) => setEndMonth(e.target.value)}
                >
                  <option value="">Select month</option>
                  {getMonthsList()
                    .filter((month) => !startMonth || month.value >= startMonth)
                    .map((month) => (
                      <option key={month.value} value={month.value}>
                        {month.label}
                      </option>
                    ))}
                </select>
              </div>
            </div>
          )}

          <div className="date-range-actions">
            <button className="clear-btn" onClick={handleClear}>
              Clear
            </button>
            <button className="apply-btn" onClick={handleApply}>
              Apply
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default DateRangePicker

