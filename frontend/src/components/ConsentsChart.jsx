import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import ChartWrapper from './ChartWrapper'
import SkeletonLoader from './SkeletonLoader'
import './ChartCard.css'

function ConsentsChart({ data, onViewData, loading = false }) {
  const COLORS = ['#3498db', '#ff9800']

  if (loading) {
    return <SkeletonLoader type="chart" />
  }

  if (!data || (data.listening === 0 && data.dictation === 0)) {
    return (
      <ChartWrapper
        title="Consents"
        empty={true}
        emptyMessage="No consent data available."
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
    { name: 'Listening Session', value: data.listening },
    { name: 'Dictation Session', value: data.dictation }
  ]

  return (
    <ChartWrapper
      title="Consents"
      tooltip="Shows the breakdown of consent types: Listening Session vs Dictation Session."
      headerAction={
        onViewData && (
          <button className="view-data-btn" onClick={onViewData} title="View detailed data">
            View Data
          </button>
        )
      }
    >
      <ResponsiveContainer width="100%" height={240}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={85}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value) => [value, 'Sessions']}
            labelFormatter={(label) => `${label} Consents`}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </ChartWrapper>
  )
}

export default ConsentsChart

