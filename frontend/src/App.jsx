import React, { useState } from 'react';
import './styles/App.css';
import Dashboard from './components/Dashboard';
import Scanner from './components/Scanner';
import Quarantine from './components/Quarantine';
import Settings from './components/Settings';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [threats, setThreats] = useState([]);

  const renderView = () => {
    switch (currentView) {
      case 'scanner':
        return <Scanner />;
      case 'quarantine':
        return <Quarantine />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard threats={threats} />;
    }
  };

  return (
    <div className="app">
      <nav className="sidebar">
        <div className="logo">🛡️ Antivirus Scanner</div>
        <ul className="nav-menu">
          <li>
            <button
              className={currentView === 'dashboard' ? 'active' : ''}
              onClick={() => setCurrentView('dashboard')}
            >
              Dashboard
            </button>
          </li>
          <li>
            <button
              className={currentView === 'scanner' ? 'active' : ''}
              onClick={() => setCurrentView('scanner')}
            >
              Scanner
            </button>
          </li>
          <li>
            <button
              className={currentView === 'quarantine' ? 'active' : ''}
              onClick={() => setCurrentView('quarantine')}
            >
              Quarantine
            </button>
          </li>
          <li>
            <button
              className={currentView === 'settings' ? 'active' : ''}
              onClick={() => setCurrentView('settings')}
            >
              Settings
            </button>
          </li>
        </ul>
      </nav>
      <main className="content">
        {renderView()}
      </main>
    </div>
  );
}

export default App;
