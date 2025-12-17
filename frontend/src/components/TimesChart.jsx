import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import ChartWrapper from './ChartWrapper'
import SkeletonLoader from './SkeletonLoader'
import './ChartCard.css'

function TimesChart({ data, loading = false }) {
  if (loading) {
    return <SkeletonLoader type="chart" />
  }

  if (!data || data.length === 0) {
    return (
      <ChartWrapper
        title="Time Breakdown"
        empty={true}
        emptyMessage="No time data available to display."
      />
    )
  }

  return (
    <ChartWrapper
      title="Time Breakdown"
      tooltip="Shows monthly breakdown of recording time, processing time, and time from creation to sign."
    >
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip 
            formatter={(value, name) => [`${value} hrs`, name]}
            labelFormatter={(label) => `Month: ${label}`}
          />
          <Legend />
          <Bar dataKey="recording" stackId="a" fill="#9b59b6" name="Recording" />
          <Bar dataKey="processing" stackId="a" fill="#ff9800" name="Processing" />
          <Bar dataKey="createdToSign" stackId="a" fill="#3498db" name="Created to Sign" />
        </BarChart>
      </ResponsiveContainer>
    </ChartWrapper>
  )
}

export default TimesChart

