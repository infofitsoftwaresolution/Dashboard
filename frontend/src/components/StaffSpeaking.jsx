import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import './ChartCard.css'

function StaffSpeaking({ data, onViewData }) {
  const COLORS = ['#ff9800', '#3498db']

  if (!data || (data.staff === 0 && data.nonStaff === 0)) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Staff Speaking</h3>
          {onViewData && <button className="view-data-btn" onClick={onViewData}>View Data</button>}
        </div>
        <div className="no-data">No data available</div>
      </div>
    )
  }

  const chartData = [
    { name: 'Non-Staff', value: data.nonStaff },
    { name: 'Staff', value: data.staff }
  ]

  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Staff Speaking</h3>
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

export default StaffSpeaking

