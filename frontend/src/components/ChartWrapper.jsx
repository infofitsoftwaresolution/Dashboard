import React from 'react'
import Card from './Card'
import SkeletonLoader from './SkeletonLoader'
import EmptyState from './EmptyState'
import './ChartWrapper.css'

function ChartWrapper({ 
  title, 
  children, 
  loading = false, 
  empty = false,
  emptyMessage = 'No data available for this chart.',
  tooltip,
  className = '',
  headerAction
}) {
  if (loading) {
    return (
      <Card title={title} className={`chart-wrapper ${className}`}>
        <SkeletonLoader type="chart" />
      </Card>
    )
  }

  if (empty) {
    return (
      <Card 
        title={title} 
        className={`chart-wrapper ${className}`}
        empty={true}
        emptyState={<EmptyState icon="📊" message={emptyMessage} />}
      />
    )
  }

  return (
    <Card 
      title={title} 
      className={`chart-wrapper ${className}`}
      headerAction={headerAction}
    >
      <div className="chart-content">
        {tooltip && (
          <div className="chart-tooltip-info" title={tooltip}>
            ℹ️
          </div>
        )}
        {children}
      </div>
    </Card>
  )
}

export default ChartWrapper

