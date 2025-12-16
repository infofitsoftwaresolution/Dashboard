import React from 'react'
import DataTable from './DataTable'
import {
  AuditStatusChart, AuditActionChart,
  PatientAccessTrendChart, PatientAccessTypeChart,
  ServiceUsageChart,
  RecommendationPriorityChart, RecommendationStatusChart,
  DeliveryFrequencyChart,
  SignedNotesTrendChart, SignedNotesStatusChart,
  PractitionerUsageChart,
  SyncIssuesSeverityChart, SyncIssuesStatusChart,
  UnsignedNotesTrendChart, UnsignedNotesByPractitionerChart
} from './SectionCharts'
import './ReportSection.css'

function ReportSection({ sectionId, data, loading, activeFilters }) {
  const getStatusBadge = (status) => {
    if (!status) return <span className="status-badge">{status || 'N/A'}</span>
    const statusClass = status.toLowerCase().replace(/\s+/g, '-')
    // Map status values to CSS classes
    const statusMap = {
      'success': 'status-success',
      'signed': 'status-signed',
      'active': 'status-active',
      'resolved': 'status-resolved',
      'completed': 'status-completed',
      'pending': 'status-pending',
      'pending-review': 'status-pending',
      'paused': 'status-paused',
      'in-progress': 'status-in-progress',
      'failed': 'status-failed',
      'open': 'status-open',
      'archived': 'status-archived',
      'closed': 'status-closed',
      'dismissed': 'status-dismissed'
    }
    const cssClass = statusMap[statusClass] || 'status-info'
    return <span className={`status-badge ${cssClass}`}>{status}</span>
  }

  const getPriorityBadge = (priority) => {
    if (!priority) return <span className="priority-badge">{priority || 'N/A'}</span>
    const priorityClass = priority.toLowerCase()
    return <span className={`priority-badge priority-${priorityClass}`}>{priority}</span>
  }

  const sections = {
    'audit': {
      title: 'Audit Summary',
      columns: [
        { key: 'date', header: 'Date' },
        { key: 'action', header: 'Action' },
        { key: 'user', header: 'User' },
        { key: 'status', header: 'Status', render: (value) => getStatusBadge(value) },
        { key: 'details', header: 'Details' }
      ]
    },
    'patient-access': {
      title: 'Patient Access',
      columns: [
        { key: 'patientId', header: 'Patient ID' },
        { key: 'patientName', header: 'Patient Name' },
        { key: 'accessDate', header: 'Access Date' },
        { key: 'accessType', header: 'Access Type' },
        { key: 'duration', header: 'Duration' }
      ]
    },
    'patient-service': {
      title: 'Patient Service Usage',
      columns: [
        { key: 'serviceName', header: 'Service Name' },
        { key: 'usageCount', header: 'Usage Count' },
        { key: 'totalTime', header: 'Total Time' },
        { key: 'lastUsed', header: 'Last Used' }
      ]
    },
    'recommendation': {
      title: 'Recommendation Summary',
      columns: [
        { key: 'id', header: 'ID' },
        { key: 'type', header: 'Type' },
        { key: 'priority', header: 'Priority', render: (value) => getPriorityBadge(value) },
        { key: 'status', header: 'Status', render: (value) => getStatusBadge(value) },
        { key: 'createdDate', header: 'Created Date' }
      ]
    },
    'delivery': {
      title: 'Report Delivery Schedules',
      columns: [
        { key: 'reportName', header: 'Report Name' },
        { key: 'frequency', header: 'Frequency' },
        { key: 'nextDelivery', header: 'Next Delivery' },
        { key: 'status', header: 'Status', render: (value) => getStatusBadge(value) }
      ]
    },
    'signed': {
      title: 'Signed Notes',
      columns: [
        { key: 'noteId', header: 'Note ID' },
        { key: 'patientName', header: 'Patient Name' },
        { key: 'practitioner', header: 'Practitioner' },
        { key: 'signedDate', header: 'Signed Date' },
        { key: 'status', header: 'Status', render: (value) => getStatusBadge(value) }
      ]
    },
    'practitioner': {
      title: 'Practitioner Service Usage',
      columns: [
        { key: 'practitionerName', header: 'Practitioner' },
        { key: 'visits', header: 'Visits' },
        { key: 'totalTime', header: 'Total Time' },
        { key: 'lastActive', header: 'Last Active' }
      ]
    },
    'sync': {
      title: 'Sync Issues',
      columns: [
        { key: 'id', header: 'Issue ID' },
        { key: 'type', header: 'Type' },
        { key: 'severity', header: 'Severity', render: (value) => getPriorityBadge(value) },
        { key: 'status', header: 'Status', render: (value) => getStatusBadge(value) },
        { key: 'reportedDate', header: 'Reported Date' }
      ]
    },
    'unsigned': {
      title: 'Unsigned Notes',
      columns: [
        { key: 'noteId', header: 'Note ID' },
        { key: 'patientName', header: 'Patient Name' },
        { key: 'practitioner', header: 'Practitioner' },
        { key: 'createdDate', header: 'Created Date' },
        { key: 'daysPending', header: 'Days Pending', render: (value) => (
          <span className={value > 7 ? 'priority-badge priority-high' : value > 3 ? 'priority-badge priority-medium' : ''}>
            {value} days
          </span>
        )}
      ]
    }
  }

  const section = sections[sectionId]
  if (!section) {
    return (
      <div className="report-section">
        <div className="report-placeholder">
          <div className="placeholder-icon">📊</div>
          <h2>Report Section</h2>
          <p>Content will be displayed here.</p>
        </div>
      </div>
    )
  }

  const renderCharts = () => {
    const filterInfo = activeFilters ? {
      practitioner: activeFilters.practitioner,
      program: activeFilters.program,
      location: activeFilters.location
    } : null
    
    switch (sectionId) {
      case 'audit':
        return (
          <div className="charts-grid-section">
            <AuditStatusChart data={data} filterInfo={filterInfo} />
            <AuditActionChart data={data} filterInfo={filterInfo} />
          </div>
        )
      case 'patient-access':
        return (
          <div className="charts-grid-section">
            <PatientAccessTrendChart data={data} filterInfo={filterInfo} />
            <PatientAccessTypeChart data={data} filterInfo={filterInfo} />
          </div>
        )
      case 'patient-service':
        return (
          <div className="charts-grid-section">
            <ServiceUsageChart data={data} filterInfo={filterInfo} />
          </div>
        )
      case 'recommendation':
        return (
          <div className="charts-grid-section">
            <RecommendationPriorityChart data={data} filterInfo={filterInfo} />
            <RecommendationStatusChart data={data} filterInfo={filterInfo} />
          </div>
        )
      case 'delivery':
        return (
          <div className="charts-grid-section">
            <DeliveryFrequencyChart data={data} filterInfo={filterInfo} />
          </div>
        )
      case 'signed':
        return (
          <div className="charts-grid-section">
            <SignedNotesTrendChart data={data} filterInfo={filterInfo} />
            <SignedNotesStatusChart data={data} filterInfo={filterInfo} />
          </div>
        )
      case 'practitioner':
        return (
          <div className="charts-grid-section">
            <PractitionerUsageChart data={data} filterInfo={filterInfo} />
          </div>
        )
      case 'sync':
        return (
          <div className="charts-grid-section">
            <SyncIssuesSeverityChart data={data} filterInfo={filterInfo} />
            <SyncIssuesStatusChart data={data} filterInfo={filterInfo} />
          </div>
        )
      case 'unsigned':
        return (
          <div className="charts-grid-section">
            <UnsignedNotesTrendChart data={data} filterInfo={filterInfo} />
            <UnsignedNotesByPractitionerChart data={data} filterInfo={filterInfo} />
          </div>
        )
      default:
        return null
    }
  }

  try {
    return (
      <div className="report-section">
        {!loading && data && data.length > 0 && renderCharts()}
        <DataTable
          title={section.title}
          columns={section.columns}
          data={data}
          loading={loading}
        />
      </div>
    )
  } catch (error) {
    console.error('Error rendering report section:', error)
    return (
      <div className="report-section">
        <div className="data-table-card">
          <h2>{section.title}</h2>
          <div className="no-data">Error loading data. Please try refreshing.</div>
        </div>
      </div>
    )
  }
}

export default ReportSection

