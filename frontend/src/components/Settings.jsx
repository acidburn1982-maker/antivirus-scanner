import React, { useState } from 'react';
import '../styles/Settings.css';

function Settings() {
  const [settings, setSettings] = useState({
    realTimeProtection: true,
    autoQuarantine: true,
    scanFrequency: 'daily'
  });

  const handleToggle = (key) => {
    setSettings(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const saveSettings = () => {
    alert('Settings saved successfully!');
  };

  return (
    <div className="settings">
      <h1>Settings</h1>
      
      <div className="settings-section">
        <h2>Protection</h2>
        
        <div className="setting-item">
          <label>Real-time Protection</label>
          <input
            type="checkbox"
            checked={settings.realTimeProtection}
            onChange={() => handleToggle('realTimeProtection')}
          />
        </div>

        <div className="setting-item">
          <label>Auto Quarantine</label>
          <input
            type="checkbox"
            checked={settings.autoQuarantine}
            onChange={() => handleToggle('autoQuarantine')}
          />
        </div>
      </div>

      <div className="settings-actions">
        <button className="btn-save" onClick={saveSettings}>Save Settings</button>
      </div>
    </div>
  );
}

export default Settings;
