import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import ChartWrapper from './ChartWrapper'
import SkeletonLoader from './SkeletonLoader'
import './ChartCard.css'

function ActiveUsers({ data, onViewData, loading = false }) {
  const COLORS = ['#3498db', '#95a5a6']

  if (loading) {
    return <SkeletonLoader type="chart" />
  }

  if (!data || (data.active === 0 && data.enabled === 0)) {
    return (
      <ChartWrapper
        title="Active vs Enabled Users"
        empty={true}
        emptyMessage="No user data available to display."
        headerAction={
          onViewData && (
            <button className="view-data-btn" onClick={onViewData} title="View detailed data">
              View Data
            </button>
          )
        }
      />
    )
  }

  const inactive = Math.max(0, data.enabled - data.active)
  const chartData = [
    { name: 'Active', value: data.active },
    { name: 'Inactive', value: inactive }
  ]

  return (
    <ChartWrapper
      title="Active vs Enabled Users"
      tooltip="Shows the breakdown of active users versus inactive users in the system."
      headerAction={
        onViewData && (
          <button className="view-data-btn" onClick={onViewData} title="View detailed data">
            View Data
          </button>
        )
      }
    >
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={70}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value) => [value, 'Users']}
            labelFormatter={(label) => `${label} Users`}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </ChartWrapper>
  )
}

export default ActiveUsers

