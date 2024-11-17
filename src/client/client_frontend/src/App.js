import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [backups, setBackups] = useState([]);

  const api_url = `http://localhost:${process.env.REACT_APP_CLIENT_PORT}/api`;

  useEffect(() => {
    axios.get(api_url + '/get_backups')
      .then(response => {
        setBackups(response.data);
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
  }, [api_url]);

  const handleDecryptClick = (backup) => {
    // Envía una petición POST al endpoint /api/decrypt_backup
    axios.post(api_url + '/decrypt_backup', { filename: backup })
    .then(response => {
      console.log(response.data);
      alert(`Decryption successful. Decrypted file: ${response.data.filename}`);
    })
    .catch(error => {
      console.error('There was an error!', error);
      alert('Decryption failed. Please check the console for more details.');
    });
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '20px' }}>
      <h1>Backups disponibles para desencriptar</h1>
      <table style={{ textAlign: 'center', margin: 'auto', width: '50%', border: '1px solid black' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid black' }}>Nombre del backup</th>
            <th style={{ border: '1px solid black' }}>Acción</th>
          </tr>
        </thead>
        <tbody>
          {backups.map((backup, index) => (
            <tr key={index}>
              <td style={{ border: '1px solid black' }}>{backup}</td>
              <td style={{ border: '1px solid black' }}>
                <button onClick={() => handleDecryptClick(backup)}>Desencriptar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;