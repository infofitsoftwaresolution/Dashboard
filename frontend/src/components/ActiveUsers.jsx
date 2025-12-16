import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import './ChartCard.css'

function ActiveUsers({ data, onViewData }) {
  const COLORS = ['#3498db', '#95a5a6']

  if (!data || (data.active === 0 && data.enabled === 0)) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Active vs Enabled Users</h3>
          {onViewData && <button className="view-data-btn" onClick={onViewData}>View Data</button>}
        </div>
        <div className="no-chart-data">
          <div className="no-data-icon">👤</div>
          <p>No data available to show the chart.</p>
        </div>
      </div>
    )
  }

  const inactive = Math.max(0, data.enabled - data.active)
  const chartData = [
    { name: 'Active', value: data.active },
    { name: 'Inactive', value: inactive }
  ]

  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Active vs Enabled Users</h3>
        {onViewData && <button className="view-data-btn" onClick={onViewData}>View Data</button>}
      </div>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
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

export default ActiveUsers

