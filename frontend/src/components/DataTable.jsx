import React from 'react'
import './DataTable.css'

function DataTable({ title, columns, data, loading }) {
  if (loading) {
    return (
      <div className="data-table-card">
        <h2>{title}</h2>
        <div className="loading-state">Loading...</div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="data-table-card">
        <div className="data-table-header">
          <h2>{title}</h2>
          <span className="record-count-badge" style={{background: '#95a5a6'}}>0 records</span>
        </div>
        <div className="no-data">
          <div className="no-data-icon">📊</div>
          <div className="no-data-message">No data available</div>
          <div className="no-data-hint">Try adjusting your filters to see more results</div>
        </div>
      </div>
    )
  }

  return (
    <div className="data-table-card">
      <div className="data-table-header">
        <h2>{title}</h2>
        <span className="record-count-badge">
          {data.length} {data.length === 1 ? 'record' : 'records'}
        </span>
      </div>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((col, index) => (
                <th key={index}>{col.header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {columns.map((col, colIndex) => {
                  try {
                    const cellValue = col.render 
                      ? col.render(row[col.key], row) 
                      : (row[col.key] ?? 'N/A')
                    return <td key={colIndex}>{cellValue}</td>
                  } catch (error) {
                    console.error(`Error rendering cell [${rowIndex}, ${colIndex}]:`, error)
                    return <td key={colIndex}>Error</td>
                  }
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default DataTable

