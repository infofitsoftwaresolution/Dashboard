import React, { useState, useEffect } from 'react'
import axios from 'axios'
import DataTable from './DataTable'
import SkeletonLoader from './SkeletonLoader'
import EmptyState from './EmptyState'
import './AthenaDataView.css'

const API_BASE_URL = 'http://localhost:8000'

function AthenaDataView({ dateRange, monthRange, selectedPractitioner, selectedProgram, selectedLocation }) {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [summary, setSummary] = useState(null)
  const [limit, setLimit] = useState(null) // null = ALL data
  const [fetchingAll, setFetchingAll] = useState(false)
  const [fileInfo, setFileInfo] = useState(null)
  const [showFileInfo, setShowFileInfo] = useState(false)

  useEffect(() => {
    fetchAthenaData()
    fetchSummary()
    fetchFileInfo()
  }, [dateRange, monthRange, limit, selectedPractitioner])

  const fetchAthenaData = async (fetchAll = false) => {
    try {
      setLoading(true)
      setError(null)
      setFetchingAll(fetchAll)
      
      const params = new URLSearchParams()
      
      // If fetching all, use the all-data endpoint, otherwise use dashboard with limit
      if (fetchAll || limit === null) {
        // Fetch ALL data
        if (dateRange) {
          params.append('start_date', dateRange.start)
          params.append('end_date', dateRange.end)
        }
        if (selectedPractitioner) {
          params.append('user_id', selectedPractitioner)
        }
        
        const response = await axios.get(`${API_BASE_URL}/api/athena/all-data?${params.toString()}`, {
          timeout: 300000 // 5 minutes for large datasets
        })
        
        if (response.data.success) {
          setData(response.data.data || [])
          console.log(`✅ Fetched ALL ${response.data.count} records from Parquet files`)
        } else {
          setError(response.data.error || 'Failed to fetch all data')
          setData([])
        }
      } else {
        // Fetch with limit
        params.append('limit', limit)
        if (dateRange) {
          params.append('start_date', dateRange.start)
          params.append('end_date', dateRange.end)
        }
        if (selectedPractitioner) {
          params.append('user_id', selectedPractitioner)
        }
        
        const response = await axios.get(`${API_BASE_URL}/api/athena/dashboard?${params.toString()}`)
        
        if (response.data.success) {
          setData(response.data.data || [])
        } else {
          setError(response.data.error || 'Failed to fetch data')
          setData([])
        }
      }
    } catch (err) {
      console.error('Error fetching Athena data:', err)
      setError(err.response?.data?.error || err.message || 'Failed to fetch data from Athena')
      setData([])
    } finally {
      setLoading(false)
      setFetchingAll(false)
    }
  }

  const fetchSummary = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/athena/summary`)
      if (response.data.success) {
        setSummary(response.data.stats)
      }
    } catch (err) {
      console.error('Error fetching summary:', err)
    }
  }

  const fetchFileInfo = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/athena/verify-files`)
      if (response.data.success) {
        setFileInfo(response.data.verification)
      }
    } catch (err) {
      console.error('Error fetching file info:', err)
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    try {
      const date = new Date(dateString)
      return date.toLocaleString()
    } catch {
      return dateString
    }
  }

  const formatDuration = (seconds) => {
    if (!seconds) return 'N/A'
    const num = parseFloat(seconds)
    if (isNaN(num)) return seconds
    const mins = Math.floor(num / 60)
    const secs = Math.floor(num % 60)
    return `${mins}m ${secs}s`
  }

  const formatNumber = (value) => {
    if (value === null || value === undefined) return 'N/A'
    return typeof value === 'number' ? value.toFixed(2) : value
  }

  // Comprehensive columns - show ALL data from Parquet files
  const columns = [
    { key: 'event_name', label: 'Event', width: '120px' },
    { key: 'pk', label: 'PK', width: '150px' },
    { key: 'sk', label: 'SK', width: '150px' },
    { key: 'app', label: 'App', width: '100px' },
    { key: 'tenant_id', label: 'Tenant', width: '150px' },
    { key: 'user_id', label: 'User ID', width: '100px' },
    { key: 'patient_id', label: 'Patient ID', width: '100px' },
    { key: 'patient_name', label: 'Patient', width: '150px' },
    { key: 'status', label: 'Status', width: '100px' },
    { key: 'status_reason', label: 'Status Reason', width: '120px' },
    { key: 'care_record_id', label: 'Care Record ID', width: '120px' },
    { key: 'appt_datetime', label: 'Appointment', width: '150px', formatter: formatDate },
    { key: 'creation_datetime', label: 'Created', width: '150px', formatter: formatDate },
    { key: 'completed_datetime', label: 'Completed', width: '150px', formatter: formatDate },
    { key: 'lastupdated_datetime', label: 'Last Updated', width: '150px', formatter: formatDate },
    { key: 'audit_datetime', label: 'Audit Date', width: '150px', formatter: formatDate },
    { key: 'submitted_datetime', label: 'Submitted', width: '150px', formatter: formatDate },
    { key: 'audio_duration', label: 'Duration', width: '100px', formatter: formatDuration },
    { key: 'similarity', label: 'Similarity', width: '100px', formatter: formatNumber },
    { key: 'note_format', label: 'Format', width: '80px' },
    { key: 'session_id', label: 'Session ID', width: '120px' },
    { key: 'creation_userid', label: 'Created By', width: '100px' },
    { key: 'lastupdated_userid', label: 'Updated By', width: '100px' },
    { key: 'lastupdated_reason', label: 'Update Reason', width: '120px' },
    { key: 'expireat', label: 'Expires At', width: '120px' },
    { key: 'audio_uri', label: 'Audio URI', width: '200px' },
    { key: 'summary_uri', label: 'Summary URI', width: '200px' },
    { key: 'transcript_uri', label: 'Transcript URI', width: '200px' }
  ]

  if (loading) {
    return <SkeletonLoader />
  }

  if (error) {
    return (
      <div className="athena-data-view">
        <div className="error-message">
          <h3>⚠️ Error Loading Athena Data</h3>
          <p>{error}</p>
          <div className="error-hint">
            <p>Make sure:</p>
            <ul>
              <li>AWS credentials are configured in backend/.env</li>
              <li>Athena table is created and accessible</li>
              <li>Backend server is running</li>
            </ul>
          </div>
          <button onClick={fetchAthenaData} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="athena-data-view">
      <div className="athena-header">
        <div className="athena-title-section">
          <h2>📊 Athena Data View</h2>
          <p className="athena-subtitle">Live data from S3 Parquet files via Athena</p>
        </div>
        
        {summary && (
          <div className="athena-summary">
            <div className="summary-item">
              <span className="summary-label">Total Records:</span>
              <span className="summary-value">{summary.total_records?.toLocaleString() || 'N/A'}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Unique Users:</span>
              <span className="summary-value">{summary.unique_users?.toLocaleString() || 'N/A'}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Unique Patients:</span>
              <span className="summary-value">{summary.unique_patients?.toLocaleString() || 'N/A'}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Unique Tenants:</span>
              <span className="summary-value">{summary.unique_tenants?.toLocaleString() || 'N/A'}</span>
            </div>
            {summary.date_range?.min_date && (
              <div className="summary-item">
                <span className="summary-label">Date Range:</span>
                <span className="summary-value">
                  {new Date(summary.date_range.min_date).toLocaleDateString()} - {new Date(summary.date_range.max_date).toLocaleDateString()}
                </span>
              </div>
            )}
            {summary.status_counts && Object.keys(summary.status_counts).length > 0 && (
              <div className="summary-item">
                <span className="summary-label">Statuses:</span>
                <span className="summary-value">
                  {Object.entries(summary.status_counts).map(([status, count]) => `${status}: ${count}`).join(', ')}
                </span>
              </div>
            )}
          </div>
        )}
      </div>

      {fileInfo && (
        <div className="athena-file-info-container">
          <button 
            className="file-info-toggle"
            onClick={() => setShowFileInfo(!showFileInfo)}
          >
            {showFileInfo ? '▼' : '▶'} 📁 Parquet Files in S3 ({fileInfo.file_count || 0} files)
          </button>
          {showFileInfo && (
            <div className="athena-file-info">
              <div className="file-info-stats">
                <div className="file-stat">
                  <strong>Total Files:</strong> {fileInfo.file_count || 0}
                </div>
                <div className="file-stat">
                  <strong>Total Size:</strong> {fileInfo.total_size_bytes ? (fileInfo.total_size_bytes / (1024 * 1024)).toFixed(2) : 0} MB
                </div>
                <div className="file-stat">
                  <strong>S3 Location:</strong> <code>{fileInfo.s3_location || 'N/A'}</code>
                </div>
              </div>
              {fileInfo.files && fileInfo.files.length > 0 && (
                <div className="file-list-container">
                  <strong>Files:</strong>
                  <ul className="file-list">
                    {fileInfo.files.map((file, idx) => (
                      <li key={idx}>
                        {file.key.split('/').pop()} ({(file.size / 1024).toFixed(2)} KB)
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <button 
                className="refresh-file-button"
                onClick={fetchFileInfo} 
              >
                🔄 Refresh File List
              </button>
            </div>
          )}
        </div>
      )}

      <div className="athena-controls">
        <div className="limit-control">
          <label>Records Limit:</label>
          <select value={limit || 'all'} onChange={(e) => setLimit(e.target.value === 'all' ? null : Number(e.target.value))}>
            <option value="all">ALL DATA (No Limit)</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
            <option value={200}>200</option>
            <option value={500}>500</option>
            <option value={1000}>1000</option>
          </select>
        </div>
        <button 
          onClick={() => fetchAthenaData(true)} 
          className="refresh-button fetch-all-button"
          disabled={fetchingAll || loading}
        >
          {fetchingAll ? '⏳ Fetching ALL Data...' : '📥 Fetch ALL Data from Parquet'}
        </button>
        <button onClick={() => fetchAthenaData(false)} className="refresh-button" disabled={loading}>
          🔄 Refresh
        </button>
      </div>

      {data.length === 0 ? (
        <EmptyState message="No data found in Athena" />
      ) : (
        <>
          <div className="data-info">
            Showing {data.length} record{data.length !== 1 ? 's' : ''} from Athena
          </div>
          <DataTable 
            data={data} 
            columns={columns}
            title="Athena Audit Trail Data"
          />
        </>
      )}
    </div>
  )
}

export default AthenaDataView

