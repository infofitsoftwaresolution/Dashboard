import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './ChartCard.css'

function TimesChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3>Times</h3>
        </div>
        <div className="no-data">No data available</div>
      </div>
    )
  }

  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Times</h3>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="recording" stackId="a" fill="#9b59b6" name="Recording" />
          <Bar dataKey="processing" stackId="a" fill="#ff9800" name="Processing" />
          <Bar dataKey="createdToSign" stackId="a" fill="#3498db" name="Created to Sign" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default TimesChart

