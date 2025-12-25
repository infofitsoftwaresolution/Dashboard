import React, { useState, useEffect } from 'react'
import axios from 'axios'
import DateRangePicker from './DateRangePicker'
import FilterDropdown from './FilterDropdown'
import './FilterBar.css'

const API_BASE_URL = 'http://localhost:8000'

function FilterBar({ onFilterChange, dateRange: propDateRange, monthRange: propMonthRange, selectedPractitioner, selectedProgram, selectedLocation }) {
  const [activeFilter, setActiveFilter] = useState('last-3-months')
  const [showPractitioner, setShowPractitioner] = useState(false)
  const [showProgram, setShowProgram] = useState(false)
  const [showLocation, setShowLocation] = useState(false)
  const [filterOptions, setFilterOptions] = useState({
    practitioners: [],
    programs: [],
    locations: []
  })

  // Fetch filter options on mount
  useEffect(() => {
    const fetchFilterOptions = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/filter-options`, {
          timeout: 60000  // 60 seconds - Athena queries can take time
        })
        if (response.data) {
          setFilterOptions({
            practitioners: response.data.practitioners || [],
            programs: response.data.programs || [],
            locations: response.data.locations || []
          })
          console.log('Filter options loaded:', {
            practitioners: response.data.practitioners?.length || 0,
            programs: response.data.programs?.length || 0,
            locations: response.data.locations?.length || 0
          })
        }
      } catch (error) {
        console.error('Error fetching filter options:', error)
        // Retry after 2 seconds
        setTimeout(() => {
          fetchFilterOptions()
        }, 2000)
      }
    }
    fetchFilterOptions()
  }, [])

  // Sync activeFilter with dateRange/monthRange props
  useEffect(() => {
    if (!propDateRange && !propMonthRange) {
      setActiveFilter('last-3-months')
    } else if (propDateRange || propMonthRange) {
      setActiveFilter('')
    }
  }, [propDateRange, propMonthRange])

  const handleFilterClick = (filterId) => {
    if (filterId === 'clear') {
      setActiveFilter('last-3-months')
      setShowPractitioner(false)
      setShowProgram(false)
      setShowLocation(false)
      if (onFilterChange) {
        onFilterChange({ type: 'clear' })
      }
    } else if (filterId === 'practitioner') {
      setShowPractitioner(!showPractitioner)
      setShowProgram(false)
      setShowLocation(false)
    } else if (filterId === 'program') {
      setShowProgram(!showProgram)
      setShowPractitioner(false)
      setShowLocation(false)
    } else if (filterId === 'location') {
      setShowLocation(!showLocation)
      setShowPractitioner(false)
      setShowProgram(false)
    } else {
      setActiveFilter(filterId)
      if (onFilterChange) {
        onFilterChange({ type: filterId })
      }
    }
  }

  const handlePractitionerSelect = (value) => {
    if (onFilterChange) {
      onFilterChange({ type: 'practitioner', value })
    }
  }

  const handleProgramSelect = (value) => {
    if (onFilterChange) {
      onFilterChange({ type: 'program', value })
    }
  }

  const handleLocationSelect = (value) => {
    if (onFilterChange) {
      onFilterChange({ type: 'location', value })
    }
  }

  const handleDateRangeChange = (range) => {
    if (range) {
      setActiveFilter('') // Clear active filter when custom date range is applied
    }
    if (onFilterChange) {
      onFilterChange({ type: 'date-range', range })
    }
  }

  const handleMonthRangeChange = (range) => {
    if (range) {
      setActiveFilter('') // Clear active filter when custom month range is applied
    }
    if (onFilterChange) {
      onFilterChange({ type: 'month-range', range })
    }
  }

  return (
    <div className="filter-bar">
      <button 
        className={`filter-btn ${activeFilter === 'last-3-months' ? 'active' : ''}`}
        onClick={() => handleFilterClick('last-3-months')}
      >
        Last 3 Months
      </button>
      <div className="filter-dropdown-wrapper">
        <button 
          className={`filter-btn ${selectedPractitioner ? 'active' : ''}`}
          onClick={() => handleFilterClick('practitioner')}
        >
          Practitioner {selectedPractitioner ? `(${selectedPractitioner})` : ''}
        </button>
        {showPractitioner && (
          <FilterDropdown
            label="Practitioner"
            options={filterOptions.practitioners}
            selectedValue={selectedPractitioner}
            onSelect={handlePractitionerSelect}
            isOpen={showPractitioner}
            onToggle={setShowPractitioner}
          />
        )}
      </div>
      <div className="filter-dropdown-wrapper">
        <button 
          className={`filter-btn ${selectedProgram ? 'active' : ''}`}
          onClick={() => handleFilterClick('program')}
        >
          Program {selectedProgram ? `(${selectedProgram})` : ''}
        </button>
        {showProgram && (
          <FilterDropdown
            label="Program"
            options={filterOptions.programs}
            selectedValue={selectedProgram}
            onSelect={handleProgramSelect}
            isOpen={showProgram}
            onToggle={setShowProgram}
          />
        )}
      </div>
      <div className="filter-dropdown-wrapper">
        <button 
          className={`filter-btn ${selectedLocation ? 'active' : ''}`}
          onClick={() => handleFilterClick('location')}
        >
          Location {selectedLocation ? `(${selectedLocation})` : ''}
        </button>
        {showLocation && (
          <FilterDropdown
            label="Location"
            options={filterOptions.locations}
            selectedValue={selectedLocation}
            onSelect={handleLocationSelect}
            isOpen={showLocation}
            onToggle={setShowLocation}
          />
        )}
      </div>
      <button 
        className="filter-btn"
        onClick={() => handleFilterClick('clear')}
      >
        Clear filters
      </button>
      <button 
        className="filter-btn"
        onClick={() => {
          alert('Saved filters feature coming soon!')
        }}
      >
        Saved filters
      </button>
      <DateRangePicker 
        onDateRangeChange={handleDateRangeChange}
        onMonthRangeChange={handleMonthRangeChange}
      />
    </div>
  )
}

export default FilterBar

