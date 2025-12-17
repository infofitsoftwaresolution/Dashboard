import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import ChartWrapper from './ChartWrapper'
import SkeletonLoader from './SkeletonLoader'
import './ChartCard.css'

function StaffSpeaking({ data, onViewData, loading = false }) {
  const COLORS = ['#ff9800', '#3498db']

  if (loading) {
    return <SkeletonLoader type="chart" />
  }

  if (!data || (data.staff === 0 && data.nonStaff === 0)) {
    return (
      <ChartWrapper
        title="Staff Speaking"
        empty={true}
        emptyMessage="No staff speaking data available."
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

  const chartData = [
    { name: 'Non-Staff', value: data.nonStaff },
    { name: 'Staff', value: data.staff }
  ]

  return (
    <ChartWrapper
      title="Staff Speaking"
      tooltip="Shows the breakdown of speaking time between staff and non-staff members."
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
            formatter={(value) => [value, 'Sessions']}
            labelFormatter={(label) => `${label} Speaking`}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </ChartWrapper>
  )
}

export default StaffSpeaking

