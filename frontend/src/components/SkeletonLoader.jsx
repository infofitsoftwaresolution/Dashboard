import React from 'react'
import './SkeletonLoader.css'

function SkeletonLoader({ type = 'card', count = 1 }) {
  const renderSkeleton = () => {
    switch (type) {
      case 'card':
        return (
          <div className="skeleton-card">
            <div className="skeleton-line skeleton-title"></div>
            <div className="skeleton-line skeleton-value"></div>
            <div className="skeleton-line skeleton-subtitle"></div>
          </div>
        )
      case 'table':
        return (
          <div className="skeleton-table">
            <div className="skeleton-line skeleton-header"></div>
            {[...Array(5)].map((_, i) => (
              <div key={i} className="skeleton-row">
                <div className="skeleton-line skeleton-cell"></div>
                <div className="skeleton-line skeleton-cell"></div>
                <div className="skeleton-line skeleton-cell"></div>
              </div>
            ))}
          </div>
        )
      case 'chart':
        return (
          <div className="skeleton-chart">
            <div className="skeleton-line skeleton-chart-title"></div>
            <div className="skeleton-chart-content"></div>
          </div>
        )
      default:
        return <div className="skeleton-line"></div>
    }
  }

  if (count > 1) {
    return (
      <div className="skeleton-container">
        {[...Array(count)].map((_, i) => (
          <React.Fragment key={i}>{renderSkeleton()}</React.Fragment>
        ))}
      </div>
    )
  }

  return renderSkeleton()
}

export default SkeletonLoader

