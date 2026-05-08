import React, { useState } from 'react';
import '../styles/Scanner.css';

function Scanner() {
  const [isScanning, setIsScanning] = useState(false);
  const [scanProgress, setScanProgress] = useState(0);
  const [scanType, setScanType] = useState('quick');
  const [results, setResults] = useState(null);

  const startScan = async () => {
    setIsScanning(true);
    setScanProgress(0);
    setResults(null);

    for (let i = 0; i <= 100; i += 10) {
      setScanProgress(i);
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    setIsScanning(false);
    setResults({
      filesScanned: 5000,
      threatsFound: 3,
      scanTime: '2m 34s'
    });
  };

  return (
    <div className="scanner">
      <h1>Scanner</h1>
      
      <div className="scan-options">
        <div className="option">
          <input
            type="radio"
            id="quick"
            name="scanType"
            value="quick"
            checked={scanType === 'quick'}
            onChange={(e) => setScanType(e.target.value)}
          />
          <label htmlFor="quick">
            <strong>Quick Scan</strong>
            <p>Scans common locations</p>
          </label>
        </div>
        
        <div className="option">
          <input
            type="radio"
            id="full"
            name="scanType"
            value="full"
            checked={scanType === 'full'}
            onChange={(e) => setScanType(e.target.value)}
          />
          <label htmlFor="full">
            <strong>Full Scan</strong>
            <p>Scans entire system</p>
          </label>
        </div>
      </div>

      <button 
        className="scan-button" 
        onClick={startScan}
        disabled={isScanning}
      >
        {isScanning ? `Scanning... ${scanProgress}%` : 'Start Scan'}
      </button>

      {isScanning && (
        <div className="progress-container">
          <div className="progress-bar">
            <div className="progress-fill" style={{width: `${scanProgress}%`}}></div>
          </div>
        </div>
      )}

      {results && (
        <div className="scan-results">
          <h2>Scan Results</h2>
          <div className="results-summary">
            <div className="result-item">
              <span className="label">Files Scanned:</span>
              <span className="value">{results.filesScanned}</span>
            </div>
            <div className="result-item">
              <span className="label">Threats Found:</span>
              <span className="value threat">{results.threatsFound}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Scanner;
