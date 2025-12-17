import React from 'react'
import Card from './Card'
import SkeletonLoader from './SkeletonLoader'
import EmptyState from './EmptyState'
import './ChartCard.css'

function TopUsers({ data, onViewData, loading = false }) {
  if (loading) {
    return <SkeletonLoader type="chart" />
  }

  return (
    <Card
      title="Top Users"
      headerAction={
        onViewData && (
          <button className="view-data-btn" onClick={onViewData} title="View detailed data">
            View Data
          </button>
        )
      }
      empty={!data || data.length === 0}
      emptyState={
        <EmptyState 
          icon="👥" 
          title="No Users Data"
          message="There are no top users to display."
        />
      }
    >
      {data && data.length > 0 && (
        <div className="top-users-list">
          {data.map((user, index) => (
            <div key={index} className="user-item">
              <div className="user-name">{user.name}</div>
              <div className="user-stats">
                <span>Visits: {user.visits}</span>
                {user.totalTime && <span>Total Time: {user.totalTime}</span>}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  )
}

export default TopUsers

