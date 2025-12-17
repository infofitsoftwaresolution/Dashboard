import React from 'react'
import './Card.css'

function Card({ 
  children, 
  title, 
  className = '', 
  headerAction,
  loading = false,
  empty = false,
  emptyState
}) {
  return (
    <div className={`card ${className}`}>
      {title && (
        <div className="card-header">
          <h3 className="card-title">{title}</h3>
          {headerAction && <div className="card-header-action">{headerAction}</div>}
        </div>
      )}
      <div className="card-content">
        {loading ? (
          <div className="card-loading">Loading...</div>
        ) : empty && emptyState ? (
          emptyState
        ) : (
          children
        )}
      </div>
    </div>
  )
}

export default Card

