import React from 'react'
import './ChartCard.css'

function TopUsers({ data, onViewData }) {
  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3>Top Users</h3>
        {onViewData && <button className="view-data-btn" onClick={onViewData}>View Data</button>}
      </div>
      <div className="top-users-list">
        {data && data.length > 0 ? (
          data.map((user, index) => (
            <div key={index} className="user-item">
              <div className="user-name">{user.name}</div>
              <div className="user-stats">
                <span>Visits: {user.visits}</span>
                {user.totalTime && <span>Total Time: {user.totalTime}</span>}
              </div>
            </div>
          ))
        ) : (
          <div className="no-data">No data available</div>
        )}
      </div>
    </div>
  )
}

export default TopUsers

