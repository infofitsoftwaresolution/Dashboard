import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import './ChartCard.css'

function ConsentsChart({ data, onViewData }) {
  const COLORS = ['#3498db', '#ff9800']

  if (!data || (data.listening === 0 && data.dictation === 0)) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Consents</h3>
          {onViewData && <button className="view-data-btn" onClick={onViewData}>View Data</button>}
        </div>
        <div className="no-data">No data available</div>
      </div>
    )
  }

  const chartData = [
    { name: 'Listening Session', value: data.listening },
    { name: 'Dictation Session', value: data.dictation }
  ]

  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Consents</h3>
        {onViewData && <button className="view-data-btn" onClick={onViewData}>View Data</button>}
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

export default ConsentsChart

