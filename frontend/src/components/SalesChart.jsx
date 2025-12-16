import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts'

function SalesChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="date" 
          tick={{ fontSize: 12 }}
          angle={-45}
          textAnchor="end"
          height={80}
        />
        <YAxis yAxisId="left" tick={{ fontSize: 12 }} />
        <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} />
        <Tooltip 
          contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
        />
        <Legend />
        <Line 
          yAxisId="left"
          type="monotone" 
          dataKey="sales" 
          stroke="#8884d8" 
          strokeWidth={2}
          name="Sales ($)"
          dot={false}
        />
        <Line 
          yAxisId="right"
          type="monotone" 
          dataKey="orders" 
          stroke="#82ca9d" 
          strokeWidth={2}
          name="Orders"
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

export default SalesChart

