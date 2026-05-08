import React, { useState } from 'react';
import '../styles/Dashboard.css';

function Dashboard({ threats }) {
  const [protectionStatus] = useState('active');

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      <div className="status-cards">
        <div className="status-card protection-status">
          <div className="status-icon">🛡️</div>
          <div className="status-info">
            <h2>Real-time Protection</h2>
            <p className={`status-text ${protectionStatus}`}>
              ✓ Active
            </p>
          </div>
        </div>

        <div className="status-card threats-found">
          <div className="status-icon">⚠️</div>
          <div className="status-info">
            <h2>Threats Found</h2>
            <p className="threat-count">{threats.length}</p>
          </div>
        </div>

        <div className="status-card last-scan">
          <div className="status-icon">📅</div>
          <div className="status-info">
            <h2>Last Scan</h2>
            <p>{new Date().toLocaleDateString()}</p>
          </div>
        </div>
      </div>

      <div className="recent-threats">
        <h2>Recent Threats</h2>
        {threats.length > 0 ? (
          <ul className="threats-list">
            {threats.slice(-5).map((threat, index) => (
              <li key={index} className="threat-item">
                <span className="threat-name">{threat.name}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="no-threats">No recent threats detected</p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
