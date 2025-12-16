import React from 'react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts'

function ActivityChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="colorUsers" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="hour" 
          tick={{ fontSize: 12 }}
          label={{ value: 'Hour of Day', position: 'insideBottom', offset: -5 }}
        />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip 
          contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
        />
        <Area 
          type="monotone" 
          dataKey="active_users" 
          stroke="#8884d8" 
          fillOpacity={1}
          fill="url(#colorUsers)"
          name="Active Users"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}

export default ActivityChart

