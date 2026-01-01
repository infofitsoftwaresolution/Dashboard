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
import SkeletonLoader from './components/SkeletonLoader'
import EmptyState from './components/EmptyState'
import Modal from './components/Modal'
import DataTable from './components/DataTable'
import AthenaDataView from './components/AthenaDataView'
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
  const [modalOpen, setModalOpen] = useState(false)
  const [modalData, setModalData] = useState({ title: '', data: [], columns: [] })

  useEffect(() => {
    if (activeSection === 'dashboard') {
      fetchDashboardData(dateRange, monthRange, selectedPractitioner, selectedProgram, selectedLocation)
    } else if (activeSection === 'athena') {
      // Athena data is fetched by the component itself
      setLoading(false)
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

  const handleViewData = (dataType, data = [], columns = []) => {
    console.log('View data clicked for:', dataType)
    setModalData({
      title: `${dataType} - Detailed View`,
      data: data,
      columns: columns
    })
    setModalOpen(true)
  }

  const handleSettings = () => {
    setShowSettings(!showSettings)
  }

  const handleEdit = () => {
    // Edit mode functionality
  }

  const handleClearFilters = () => {
    setDateRange(null)
    setMonthRange(null)
    setSelectedPractitioner(null)
    setSelectedProgram(null)
    setSelectedLocation(null)
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
      'athena': 'Athena Data View',
      'audit': 'Audit Trail Summary',
      'patient-access': 'Patient Access Logs',
      'patient-service': 'Patient Service Usage',
      'recommendation': 'Similarity Recommendations',
      'delivery': 'Report Schedules',
      'signed': 'Finalized Notes',
      'practitioner': 'Practitioner Activity',
      'sync': 'Session Sync Issues',
      'unsigned': 'Pending Notes'
    }
    return titles[section] || 'Report'
  }

  const renderContent = () => {
    if (activeSection === 'athena') {
      return (
        <AthenaDataView
          dateRange={dateRange}
          monthRange={monthRange}
          selectedPractitioner={selectedPractitioner}
          selectedProgram={selectedProgram}
          selectedLocation={selectedLocation}
        />
      )
    }
    
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
        <>
          <FilterIndicator
            dateRange={dateRange}
            monthRange={monthRange}
            practitioner={selectedPractitioner}
            program={selectedProgram}
            location={selectedLocation}
            recordCount={null}
            onClear={handleClearFilter}
          />
          <div className="metrics-grid">
            <SkeletonLoader type="card" count={5} />
          </div>
          <div className="charts-grid-top">
            <SkeletonLoader type="chart" />
            <SkeletonLoader type="chart" />
            <SkeletonLoader type="chart" />
          </div>
          <div className="charts-grid-bottom">
            <SkeletonLoader type="chart" />
            <SkeletonLoader type="chart" />
          </div>
        </>
      )
    }

    return (
      <>
        <FilterIndicator
          dateRange={dateRange}
          monthRange={monthRange}
          practitioner={selectedPractitioner}
          program={selectedProgram}
          location={selectedLocation}
          recordCount={null}
          onClear={handleClearFilter}
        />
        
        <div className="metrics-grid">
          {metrics.length > 0 ? (
            metrics.map((metric, index) => (
              <MetricCard key={index} metric={metric} />
            ))
          ) : (
            <EmptyState 
              icon="📊" 
              title="No Metrics Available"
              message="There are no metrics to display. Try adjusting your filters."
            />
          )}
        </div>

        <div className="charts-grid-top">
          <TopUsers 
            data={topUsers} 
            loading={loading}
            onViewData={() => handleViewData('Top Users', topUsers, ['name', 'visits', 'total_time'])} 
          />
          <ActiveUsers 
            data={activeUsers} 
            loading={loading}
            onViewData={() => handleViewData('Active Users', [activeUsers], ['active', 'enabled'])} 
          />
          <StaffSpeaking 
            data={staffSpeaking} 
            loading={loading}
            onViewData={() => handleViewData('Staff Speaking', [staffSpeaking], ['staff', 'nonStaff'])} 
          />
        </div>

        <div className="charts-grid-bottom">
          <TimesChart data={timesData} loading={loading} />
          <ConsentsChart 
            data={consentsData} 
            loading={loading}
            onViewData={() => handleViewData('Consents', [consentsData], ['listening', 'dictation'])} 
          />
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
      <Header 
        dateRange={dateRange}
        monthRange={monthRange}
        selectedPractitioner={selectedPractitioner}
        selectedProgram={selectedProgram}
        selectedLocation={selectedLocation}
        onFilterChange={handleFilterChange}
        onClearFilters={handleClearFilters}
      />
      <div className="main-content">
        <div className="content-wrapper">
          {renderContent()}
        </div>
      </div>
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title={modalData.title}
        size="large"
      >
        <DataTable
          data={modalData.data}
          columns={modalData.columns}
          title=""
        />
      </Modal>
    </div>
  )
}

export default App

