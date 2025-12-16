import React from 'react'
import './MetricCard.css'

function MetricCard({ metric }) {
  const isPositive = metric.change > 0
  const trendIcon = metric.trend === 'up' ? '↑' : '↓'
  const changeColor = isPositive ? '#27ae60' : '#e74c3c'

  const formatValue = (value, label) => {
    if (typeof value === 'string') return value
    // Handle percentage values (like "Note Content from Scribe")
    if (label && label.toLowerCase().includes('content') && label.toLowerCase().includes('scribe')) {
      return `${value.toFixed(1)}%`
    }
    if (value % 1 === 0) {
      return value.toLocaleString()
    }
    // For decimal values less than 1, treat as percentage
    if (value < 1) {
      return `${(value * 100).toFixed(1)}%`
    }
    return value.toLocaleString('en-US', { 
      style: 'currency', 
      currency: 'USD', 
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    })
  }

  return (
    <div className="metric-card">
      <div className="metric-label">{metric.label}</div>
      <div className="metric-value">{formatValue(metric.value, metric.label)}</div>
      <div className="metric-change" style={{ color: changeColor }}>
        <span className="change-percent">
          {isPositive ? '+' : ''}{metric.change.toFixed(1)}% {trendIcon}
        </span>
      </div>
    </div>
  )
}

export default MetricCard

