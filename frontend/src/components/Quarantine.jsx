import React, { useState } from 'react';
import '../styles/Quarantine.css';

function Quarantine() {
  const [quarantinedFiles, setQuarantinedFiles] = useState([
    {
      id: 1,
      name: 'malware.exe',
      threat: 'Trojan.GenericA',
      date: '2024-01-15 10:30:45'
    },
    {
      id: 2,
      name: 'worm.dll',
      threat: 'Worm.BasicWorm',
      date: '2024-01-14 14:22:15'
    }
  ]);

  const deleteFile = (id) => {
    setQuarantinedFiles(quarantinedFiles.filter(file => file.id !== id));
  };

  return (
    <div className="quarantine">
      <h1>Quarantine</h1>
      
      <div className="quarantine-stats">
        <p>Total Quarantined Items: <strong>{quarantinedFiles.length}</strong></p>
      </div>

      {quarantinedFiles.length > 0 ? (
        <table className="quarantine-table">
          <thead>
            <tr>
              <th>Filename</th>
              <th>Threat Name</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {quarantinedFiles.map(file => (
              <tr key={file.id}>
                <td>{file.name}</td>
                <td className="threat-badge">{file.threat}</td>
                <td>{file.date}</td>
                <td className="actions">
                  <button className="btn-delete" onClick={() => deleteFile(file.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className="no-files">No quarantined files</p>
      )}
    </div>
  );
}

export default Quarantine;
