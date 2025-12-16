import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import FilterBar from './components/FilterBar'
import FilterIndicator from './components/FilterIndicator'
import ReportSection from './components/ReportSection'
import MetricCard from './components/MetricCard'
import TopUsers from './components/TopUsers'
import ActiveUsers from './components/ActiveUsers'
import StaffSpeaking from './components/StaffSpeaking'
import TimesChart from './components/TimesChart'
import ConsentsChart from './components/ConsentsChart'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [activeSection, setActiveSection] = useState('dashboard')
  const [metrics, setMetrics] = useState([])
  const [topUsers, setTopUsers] = useState([])
  const [activeUsers, setActiveUsers] = useState({ active: 0, enabled: 0 })
  const [staffSpeaking, setStaffSpeaking] = useState({ staff: 0, nonStaff: 0 })
  const [timesData, setTimesData] = useState([])
  const [consentsData, setConsentsData] = useState({ listening: 0, dictation: 0 })
  const [sectionData, setSectionData] = useState([])
  const [loading, setLoading] = useState(true)
  const [showSettings, setShowSettings] = useState(false)
  const [dateRange, setDateRange] = useState(null)
  const [monthRange, setMonthRange] = useState(null)
  const [selectedPractitioner, setSelectedPractitioner] = useState(null)
  const [selectedProgram, setSelectedProgram] = useState(null)
  const [selectedLocation, setSelectedLocation] = useState(null)

  useEffect(() => {
    if (activeSection === 'dashboard') {
      fetchDashboardData(dateRange, monthRange, selectedPractitioner, selectedProgram, selectedLocation)
    } else {
      fetchSectionData(activeSection, dateRange, monthRange, selectedPractitioner, selectedProgram, selectedLocation)
    }
  }, [activeSection, dateRange, monthRange, selectedPractitioner, selectedProgram, selectedLocation])

  const fetchDashboardData = async (dateRangeFilter = null, monthRangeFilter = null, practitioner = null, program = null, location = null) => {
    try {
      setLoading(true)
      
      // Build query parameters for filters
      const params = new URLSearchParams()
      if (dateRangeFilter) {
        params.append('start_date', dateRangeFilter.start)
        params.append('end_date', dateRangeFilter.end)
      } else if (monthRangeFilter) {
        params.append('start_month', monthRangeFilter.start)
        params.append('end_month', monthRangeFilter.end)
      }
      if (practitioner) {
        params.append('practitioner', practitioner)
      }
      if (program) {
        params.append('program', program)
      }
      if (location) {
        params.append('location', location)
      }
      
      const queryString = params.toString()
      const urlSuffix = queryString ? `?${queryString}` : ''
      
      const [
        metricsRes,
        topUsersRes,
        activeUsersRes,
        staffSpeakingRes,
        timesRes,
        consentsRes
      ] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/metrics${urlSuffix}`),
        axios.get(`${API_BASE_URL}/api/top-users${urlSuffix}`),
        axios.get(`${API_BASE_URL}/api/active-users${urlSuffix}`),
        axios.get(`${API_BASE_URL}/api/staff-speaking${urlSuffix}`),
        axios.get(`${API_BASE_URL}/api/times${urlSuffix}`),
        axios.get(`${API_BASE_URL}/api/consents${urlSuffix}`)
      ])

      setMetrics(metricsRes.data || [])
      setTopUsers(topUsersRes.data || [])
      setActiveUsers(activeUsersRes.data || { active: 0, enabled: 0 })
      setStaffSpeaking(staffSpeakingRes.data || { staff: 0, nonStaff: 0 })
      setTimesData(timesRes.data || [])
      setConsentsData(consentsRes.data || { listening: 0, dictation: 0 })
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
      // Set default values on error
      setMetrics([])
      setTopUsers([])
      setActiveUsers({ active: 0, enabled: 0 })
      setStaffSpeaking({ staff: 0, nonStaff: 0 })
      setTimesData([])
      setConsentsData({ listening: 0, dictation: 0 })
    } finally {
      setLoading(false)
    }
  }

  const handleClearFilter = (filterType) => {
    if (filterType === 'date') {
      setDateRange(null)
    } else if (filterType === 'month') {
      setMonthRange(null)
    } else if (filterType === 'practitioner') {
      setSelectedPractitioner(null)
    } else if (filterType === 'program') {
      setSelectedProgram(null)
    } else if (filterType === 'location') {
      setSelectedLocation(null)
    } else if (filterType === 'all') {
      // Clear all
      setDateRange(null)
      setMonthRange(null)
      setSelectedPractitioner(null)
      setSelectedProgram(null)
      setSelectedLocation(null)
    }
  }

  const handleFilterChange = (filter) => {
    console.log('Filter changed:', filter)
    
    if (filter.type === 'clear') {
      setDateRange(null)
      setMonthRange(null)
      setSelectedPractitioner(null)
      setSelectedProgram(null)
      setSelectedLocation(null)
      // useEffect will trigger data refresh automatically
    } else if (filter.type === 'last-3-months') {
      // Calculate last 3 months date range
      const endDate = new Date()
      const startDate = new Date()
      startDate.setMonth(startDate.getMonth() - 3)
      
      const dateRange = {
        start: startDate.toISOString().split('T')[0],
        end: endDate.toISOString().split('T')[0]
      }
      
      setDateRange(dateRange)
      setMonthRange(null)
      console.log('Last 3 months selected:', dateRange)
      // useEffect will trigger data refresh automatically
    } else if (filter.type === 'date-range' && filter.range) {
      setDateRange(filter.range)
      setMonthRange(null)
      console.log('Date range selected:', filter.range)
      // useEffect will trigger data refresh automatically
    } else if (filter.type === 'month-range' && filter.range) {
      setMonthRange(filter.range)
      setDateRange(null)
      console.log('Month range selected:', filter.range)
      // useEffect will trigger data refresh automatically
    } else if (filter.type === 'practitioner') {
      setSelectedPractitioner(filter.value || null)
      console.log('Practitioner selected:', filter.value)
      // useEffect will trigger data refresh automatically
    } else if (filter.type === 'program') {
      setSelectedProgram(filter.value || null)
      console.log('Program selected:', filter.value)
      // useEffect will trigger data refresh automatically
    } else if (filter.type === 'location') {
      setSelectedLocation(filter.value || null)
      console.log('Location selected:', filter.value)
      // useEffect will trigger data refresh automatically
    } else {
      console.log('Filter applied:', filter.type)
      // In a real app, this would apply the filter
    }
  }

  const handleViewData = (dataType) => {
    console.log('View data clicked for:', dataType)
    // In a real app, this would open a detailed view or modal
    alert(`View detailed data for ${dataType}. This feature will open a detailed view.`)
  }

  const handleSettings = () => {
    setShowSettings(!showSettings)
    alert('Settings panel will open here. Configure your dashboard preferences.')
  }

  const handleEdit = () => {
    alert('Edit mode will be activated here. Customize your dashboard layout.')
  }

  const fetchSectionData = async (section, dateRange = null, monthRange = null, practitioner = null, program = null, location = null) => {
    try {
      setLoading(true)
      const endpointMap = {
        'audit': '/api/audit-summary',
        'patient-access': '/api/patient-access',
        'patient-service': '/api/patient-service-usage',
        'recommendation': '/api/recommendation-summary',
        'delivery': '/api/delivery-schedules',
        'signed': '/api/signed-notes',
        'practitioner': '/api/practitioner-service-usage',
        'sync': '/api/sync-issues',
        'unsigned': '/api/unsigned-notes'
      }

      const endpoint = endpointMap[section]
      if (endpoint) {
        let url = `${API_BASE_URL}${endpoint}`
        const params = new URLSearchParams()
        
        // Add date range or month range to query params
        if (dateRange) {
          params.append('start_date', dateRange.start)
          params.append('end_date', dateRange.end)
        } else if (monthRange) {
          params.append('start_month', monthRange.start)
          params.append('end_month', monthRange.end)
        }
        
        // Add practitioner, program, location filters
        if (practitioner) {
          params.append('practitioner', practitioner)
        }
        if (program) {
          params.append('program', program)
        }
        if (location) {
          params.append('location', location)
        }
        
        if (params.toString()) {
          url += `?${params.toString()}`
        }
        
        const response = await axios.get(url)
        setSectionData(response.data || [])
      } else {
        setSectionData([])
      }
    } catch (error) {
      console.error(`Error fetching ${section} data:`, error)
      setSectionData([])
    } finally {
      setLoading(false)
    }
  }

  const getSectionTitle = (section) => {
    const titles = {
      'audit': 'Audit Summary',
      'patient-access': 'Patient Access',
      'patient-service': 'Patient Service Usage',
      'recommendation': 'Recommendation Summary',
      'delivery': 'Report Delivery Schedules',
      'signed': 'Signed Notes',
      'practitioner': 'Practitioner Service Usage',
      'sync': 'Sync Issues',
      'unsigned': 'Unsigned Notes'
    }
    return titles[section] || 'Report'
  }

  const renderContent = () => {
    if (activeSection !== 'dashboard') {
      return (
        <>
          <div className="page-header">
            <h1 className="page-title">{getSectionTitle(activeSection)}</h1>
            <button onClick={() => fetchSectionData(activeSection, dateRange, monthRange, selectedPractitioner, selectedProgram, selectedLocation)} className="refresh-btn" title="Refresh data">
              🔄 Refresh
            </button>
          </div>
          <FilterIndicator
            dateRange={dateRange}
            monthRange={monthRange}
            practitioner={selectedPractitioner}
            program={selectedProgram}
            location={selectedLocation}
            recordCount={sectionData.length}
            onClear={handleClearFilter}
          />
          <ReportSection 
            sectionId={activeSection} 
            data={sectionData} 
            loading={loading}
            activeFilters={{
              practitioner: selectedPractitioner,
              program: selectedProgram,
              location: selectedLocation
            }}
          />
        </>
      )
    }

    if (loading) {
      return (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      )
    }

    return (
      <>
        <div className="page-header">
          <h1 className="page-title">Dashboard</h1>
          <button onClick={() => fetchDashboardData(dateRange, monthRange, selectedPractitioner, selectedProgram, selectedLocation)} className="refresh-btn" title="Refresh data">
            🔄 Refresh
          </button>
        </div>
        <FilterBar 
          onFilterChange={handleFilterChange} 
          dateRange={dateRange} 
          monthRange={monthRange}
          selectedPractitioner={selectedPractitioner}
          selectedProgram={selectedProgram}
          selectedLocation={selectedLocation}
        />
        
        <FilterIndicator
          dateRange={dateRange}
          monthRange={monthRange}
          practitioner={selectedPractitioner}
          program={selectedProgram}
          location={selectedLocation}
          recordCount={sectionData.length > 0 ? sectionData.length : (activeSection === 'dashboard' ? null : 0)}
          onClear={handleClearFilter}
        />
        
        <div className="metrics-grid">
          {metrics.map((metric, index) => (
            <MetricCard key={index} metric={metric} />
          ))}
        </div>

        <div className="charts-grid-top">
          <TopUsers data={topUsers} onViewData={() => handleViewData('Top Users')} />
          <ActiveUsers data={activeUsers} onViewData={() => handleViewData('Active Users')} />
          <StaffSpeaking data={staffSpeaking} onViewData={() => handleViewData('Staff Speaking')} />
        </div>

        <div className="charts-grid-bottom">
          <TimesChart data={timesData} />
          <ConsentsChart data={consentsData} onViewData={() => handleViewData('Consents')} />
        </div>
      </>
    )
  }

  return (
    <div className="app">
      <Sidebar 
        activeSection={activeSection} 
        onSectionChange={setActiveSection}
        onSettings={handleSettings}
        onEdit={handleEdit}
      />
      <Header />
      <div className="main-content">
        <div className="content-wrapper">
          {renderContent()}
        </div>
      </div>
    </div>
  )
}

export default App

