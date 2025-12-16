import React from 'react'
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts'
import './ChartCard.css'

const COLORS = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#95a5a6']

// Audit Summary Charts
export function AuditStatusChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Status Distribution</h3>
          <span className="chart-no-data">No data available</span>
        </div>
      </div>
    )
  }
  
  const statusCounts = data.reduce((acc, item) => {
    acc[item.status] = (acc[item.status] || 0) + 1
    return acc
  }, {})
  
  const chartData = Object.entries(statusCounts).map(([name, value]) => ({ name, value }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Status Distribution</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

export function AuditActionChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Action Types</h3>
          <span className="chart-no-data">No data available</span>
        </div>
      </div>
    )
  }
  
  // Group by practitioner and action
  const practitionerActionData = data.reduce((acc, item) => {
    const practitioner = item.practitioner || 'Unknown'
    const action = item.action || 'Unknown'
    if (!acc[practitioner]) acc[practitioner] = {}
    acc[practitioner][action] = (acc[practitioner][action] || 0) + 1
    return acc
  }, {})
  
  const practitioners = Object.keys(practitionerActionData)
  const allActions = new Set()
  Object.values(practitionerActionData).forEach(actions => {
    Object.keys(actions).forEach(action => allActions.add(action))
  })
  
  const chartData = Array.from(allActions)
    .map(action => {
      const entry = { action }
      practitioners.forEach(practitioner => {
        const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
        entry[shortName] = practitionerActionData[practitioner][action] || 0
      })
      return entry
    })
    .sort((a, b) => {
      const totalA = practitioners.reduce((sum, p) => {
        const shortName = p.split(' ').slice(-1)[0] || p
        return sum + (a[shortName] || 0)
      }, 0)
      const totalB = practitioners.reduce((sum, p) => {
        const shortName = p.split(' ').slice(-1)[0] || p
        return sum + (b[shortName] || 0)
      }, 0)
      return totalB - totalA
    })
    .slice(0, 6)
  
  const practitionerColors = ['#9b59b6', '#3498db', '#2ecc71', '#e74c3c', '#f39c12']
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Action Types by Practitioner</h3>
        {practitioners.length > 0 && (
          <span className="chart-subtitle">{data.length} total actions</span>
        )}
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="action" angle={-45} textAnchor="end" height={100} />
          <YAxis />
          <Tooltip />
          <Legend />
          {practitioners.map((practitioner, index) => {
            const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
            return (
              <Bar 
                key={practitioner}
                dataKey={shortName} 
                fill={practitionerColors[index % practitionerColors.length]}
                name={practitioner}
              />
            )
          })}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Patient Access Charts
export function PatientAccessTrendChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Access Trends (Last 14 Days)</h3>
          <span className="chart-no-data">No data available</span>
        </div>
      </div>
    )
  }
  
  // Group by practitioner for better visualization
  const practitionerData = data.reduce((acc, item) => {
    if (!item.accessDate) return acc
    const date = item.accessDate.split(' ')[0]
    if (!date) return acc
    const practitioner = item.practitioner || 'Unknown'
    if (!acc[practitioner]) acc[practitioner] = {}
    acc[practitioner][date] = (acc[practitioner][date] || 0) + 1
    return acc
  }, {})
  
  // Get all unique dates
  const allDates = new Set()
  Object.values(practitionerData).forEach(dates => {
    Object.keys(dates).forEach(date => allDates.add(date))
  })
  
  const sortedDates = Array.from(allDates).sort().slice(-14)
  
  // Create chart data with practitioner breakdown
  const chartData = sortedDates.map(date => {
    const entry = { date: date.split('-').slice(1).join('/') }
    Object.keys(practitionerData).forEach(practitioner => {
      const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
      entry[shortName] = practitionerData[practitioner][date] || 0
    })
    return entry
  })
  
  const practitioners = Object.keys(practitionerData)
  const practitionerColors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Access Trends by Practitioner (Last 14 Days)</h3>
        {practitioners.length > 0 && (
          <span className="chart-subtitle">{data.length} total accesses</span>
        )}
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" angle={-45} textAnchor="end" height={80} />
          <YAxis />
          <Tooltip />
          <Legend />
          {practitioners.map((practitioner, index) => {
            const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
            return (
              <Area 
                key={practitioner}
                type="monotone" 
                dataKey={shortName} 
                stackId="1"
                stroke={practitionerColors[index % practitionerColors.length]} 
                fill={practitionerColors[index % practitionerColors.length]}
                fillOpacity={0.6}
                name={practitioner}
              />
            )
          })}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

export function PatientAccessTypeChart({ data }) {
  if (!data || data.length === 0) return null
  
  const typeCounts = data.reduce((acc, item) => {
    acc[item.accessType] = (acc[item.accessType] || 0) + 1
    return acc
  }, {})
  
  const chartData = Object.entries(typeCounts).map(([name, value]) => ({ name, value }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Access Type Distribution</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

// Patient Service Usage Chart
export function ServiceUsageChart({ data }) {
  if (!data || data.length === 0) return null
  
  const chartData = data
    .filter(item => item.serviceName && item.usageCount !== undefined)
    .map(item => ({
      name: item.serviceName,
      usage: item.usageCount || 0
    }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Service Usage Comparison</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
          <YAxis />
          <Tooltip />
          <Bar dataKey="usage" fill="#2ecc71" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Recommendation Summary Charts
export function RecommendationPriorityChart({ data }) {
  if (!data || data.length === 0) return null
  
  const priorityCounts = data.reduce((acc, item) => {
    acc[item.priority] = (acc[item.priority] || 0) + 1
    return acc
  }, {})
  
  const chartData = Object.entries(priorityCounts).map(([name, value]) => ({ name, value }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Priority Distribution</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#f39c12" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function RecommendationStatusChart({ data }) {
  if (!data || data.length === 0) return null
  
  const statusCounts = data.reduce((acc, item) => {
    acc[item.status] = (acc[item.status] || 0) + 1
    return acc
  }, {})
  
  const chartData = Object.entries(statusCounts).map(([name, value]) => ({ name, value }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Status Breakdown</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

// Delivery Schedules Chart
export function DeliveryFrequencyChart({ data }) {
  if (!data || data.length === 0) return null
  
  const freqCounts = data.reduce((acc, item) => {
    acc[item.frequency] = (acc[item.frequency] || 0) + 1
    return acc
  }, {})
  
  const chartData = Object.entries(freqCounts).map(([name, value]) => ({ name, value }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Frequency Distribution</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#9b59b6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Signed Notes Charts
export function SignedNotesTrendChart({ data, filterInfo }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Signing Trends (Last 14 Days)</h3>
          <span className="chart-no-data">No data available</span>
        </div>
      </div>
    )
  }
  
  const filterLabel = filterInfo?.practitioner 
    ? ` - ${filterInfo.practitioner}` 
    : filterInfo?.program 
    ? ` - ${filterInfo.program}` 
    : filterInfo?.location 
    ? ` - ${filterInfo.location}` 
    : ''
  
  // Group by practitioner and date for better visualization
  const practitionerData = data.reduce((acc, item) => {
    if (!item.signedDate) return acc
    const practitioner = item.practitioner || 'Unknown'
    if (!acc[practitioner]) acc[practitioner] = {}
    acc[practitioner][item.signedDate] = (acc[practitioner][item.signedDate] || 0) + 1
    return acc
  }, {})
  
  // Get all unique dates
  const allDates = new Set()
  Object.values(practitionerData).forEach(dates => {
    Object.keys(dates).forEach(date => allDates.add(date))
  })
  
  const sortedDates = Array.from(allDates).sort().slice(-14)
  
  // Create chart data with practitioner breakdown
  const chartData = sortedDates.map(date => {
    const entry = { date: date.split('T')[0] }
    Object.keys(practitionerData).forEach(practitioner => {
      entry[practitioner.split(' ').slice(-1)[0] || practitioner] = practitionerData[practitioner][date] || 0
    })
    return entry
  })
  
  const practitioners = Object.keys(practitionerData)
  const practitionerColors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Signing Trends by Practitioner (Last 14 Days){filterLabel}</h3>
        {practitioners.length > 0 && (
          <span className="chart-subtitle">{data.length} total notes</span>
        )}
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" angle={-45} textAnchor="end" height={80} />
          <YAxis />
          <Tooltip />
          <Legend />
          {practitioners.map((practitioner, index) => {
            const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
            return (
              <Line 
                key={practitioner}
                type="monotone" 
                dataKey={shortName} 
                stroke={practitionerColors[index % practitionerColors.length]} 
                strokeWidth={2}
                name={practitioner}
              />
            )
          })}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export function SignedNotesStatusChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Status Distribution</h3>
          <span className="chart-no-data">No data available</span>
        </div>
      </div>
    )
  }
  
  // Group by practitioner and status for better breakdown
  const practitionerStatusData = data.reduce((acc, item) => {
    const practitioner = item.practitioner || 'Unknown'
    const status = item.status || 'Unknown'
    if (!acc[practitioner]) acc[practitioner] = {}
    acc[practitioner][status] = (acc[practitioner][status] || 0) + 1
    return acc
  }, {})
  
  // If only one practitioner, show simple pie chart
  const practitioners = Object.keys(practitionerStatusData)
  if (practitioners.length === 1) {
    const statusCounts = practitionerStatusData[practitioners[0]]
    const chartData = Object.entries(statusCounts).map(([name, value]) => ({ name, value }))
    
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Status Distribution - {practitioners[0]}</h3>
          <span className="chart-subtitle">{data.length} notes</span>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    )
  }
  
  // Multiple practitioners - show bar chart comparison
  const allStatuses = new Set()
  Object.values(practitionerStatusData).forEach(statuses => {
    Object.keys(statuses).forEach(status => allStatuses.add(status))
  })
  
  const chartData = Array.from(allStatuses).map(status => {
    const entry = { status }
    practitioners.forEach(practitioner => {
      const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
      entry[shortName] = practitionerStatusData[practitioner][status] || 0
    })
    return entry
  })
  
  const practitionerColors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Status Distribution by Practitioner</h3>
        <span className="chart-subtitle">{data.length} total notes</span>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="status" />
          <YAxis />
          <Tooltip />
          <Legend />
          {practitioners.map((practitioner, index) => {
            const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
            return (
              <Bar 
                key={practitioner}
                dataKey={shortName} 
                fill={practitionerColors[index % practitionerColors.length]}
                name={practitioner}
              />
            )
          })}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Practitioner Usage Chart
export function PractitionerUsageChart({ data }) {
  if (!data || data.length === 0) return null
  
  const chartData = data
    .filter(item => item.practitionerName && item.visits !== undefined)
    .map(item => ({
      name: item.practitionerName.split(' ').slice(-1)[0] || item.practitionerName,
      visits: item.visits || 0
    }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Practitioner Visits Comparison</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="visits" fill="#3498db" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Sync Issues Charts
export function SyncIssuesSeverityChart({ data }) {
  if (!data || data.length === 0) return null
  
  const severityCounts = data.reduce((acc, item) => {
    acc[item.severity] = (acc[item.severity] || 0) + 1
    return acc
  }, {})
  
  const chartData = Object.entries(severityCounts).map(([name, value]) => ({ name, value }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Severity Distribution</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#e74c3c" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function SyncIssuesStatusChart({ data }) {
  if (!data || data.length === 0) return null
  
  const statusCounts = data.reduce((acc, item) => {
    acc[item.status] = (acc[item.status] || 0) + 1
    return acc
  }, {})
  
  const chartData = Object.entries(statusCounts).map(([name, value]) => ({ name, value }))
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Status Breakdown</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

// Unsigned Notes Charts
export function UnsignedNotesTrendChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Days Pending Distribution</h3>
          <span className="chart-no-data">No data available</span>
        </div>
      </div>
    )
  }
  
  // Group by practitioner and pending range
  const practitionerPendingData = data.reduce((acc, item) => {
    if (item.daysPending === undefined || item.daysPending === null) return acc
    const practitioner = item.practitioner || 'Unknown'
    let range = '0-3 days'
    if (item.daysPending > 7) range = '8+ days'
    else if (item.daysPending > 3) range = '4-7 days'
    
    if (!acc[practitioner]) acc[practitioner] = {}
    acc[practitioner][range] = (acc[practitioner][range] || 0) + 1
    return acc
  }, {})
  
  const practitioners = Object.keys(practitionerPendingData)
  const allRanges = ['0-3 days', '4-7 days', '8+ days']
  
  const chartData = allRanges.map(range => {
    const entry = { range }
    practitioners.forEach(practitioner => {
      const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
      entry[shortName] = practitionerPendingData[practitioner][range] || 0
    })
    return entry
  })
  
  const practitionerColors = ['#e67e22', '#e74c3c', '#f39c12', '#3498db', '#2ecc71']
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Days Pending by Practitioner</h3>
        {practitioners.length > 0 && (
          <span className="chart-subtitle">{data.length} total unsigned notes</span>
        )}
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="range" />
          <YAxis />
          <Tooltip />
          <Legend />
          {practitioners.map((practitioner, index) => {
            const shortName = practitioner.split(' ').slice(-1)[0] || practitioner
            return (
              <Bar 
                key={practitioner}
                dataKey={shortName} 
                fill={practitionerColors[index % practitionerColors.length]}
                name={practitioner}
              />
            )
          })}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function UnsignedNotesByPractitionerChart({ data }) {
  if (!data || data.length === 0) return null
  
  const practitionerCounts = data.reduce((acc, item) => {
    if (!item.practitioner) return acc
    acc[item.practitioner] = (acc[item.practitioner] || 0) + 1
    return acc
  }, {})
  
  const chartData = Object.entries(practitionerCounts)
    .map(([name, value]) => ({ 
      name: name && name.split(' ').length > 0 ? name.split(' ').slice(-1)[0] : name, 
      value 
    }))
    .sort((a, b) => b.value - a.value)
  
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Unsigned Notes by Practitioner</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#e74c3c" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

