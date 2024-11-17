import React, { useState, useEffect } from 'react';
import BackupItem from './BackupItem';
import axios from 'axios';

const BackupList = () => {
  const [backups, setBackups] = useState([]);
  const [totalBackups, setTotalBackups] = useState(0);

  useEffect(() => {
    const fetchBackups = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/get_backups');
        const { backups, total } = response.data;
        setBackups(backups);
        setTotalBackups(total);
      } catch (error) {
        console.error('Error fetching backups:', error);
      }
    };

    fetchBackups();
  }, []);

  const deleteBackup = async (backupName, owner) => {
    try {
      await axios.post('http://localhost:5000/api/delete_backup', {
        backup_name: backupName,
        owner: owner,
      });
      setBackups(backups.filter((backup) => backup.name !== backupName));
      setTotalBackups(totalBackups - 1);
    } catch (error) {
      console.error('Error deleting backup:', error);
    }
  };

  const groupByOwner = (backups) => {
    return backups.reduce((groups, backup) => {
      const owner = backup.owner;
      if (!groups[owner]) {
        groups[owner] = [];
      }
      groups[owner].push(backup);
      return groups;
    }, {});
  };

  const groupedBackups = groupByOwner(backups);

  return (
    <div>
      <h2>Estado de los backups ({totalBackups})</h2>
      {backups.length > 0 ? (
        Object.keys(groupedBackups).map((owner) => (
          <div key={owner}>
            <h3>____________________________________________________________________________________</h3>
            <h3>Propietario: {owner}</h3>
            <div style={{ display: 'flex', justifyContent: 'center' }}>
              <table style={{ borderSpacing: '15px 0' }}>
                <thead>
                  <tr>
                    <th>Nombre del backup</th>
                    <th>Fecha de modificación</th>
                    <th>Tamaño del backup</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {groupedBackups[owner].map((backup) => (
                    <BackupItem
                      key={backup.name}
                      backup={backup}
                      onDelete={deleteBackup}
                      size={backup.size}
                    />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))
      ) : (
        <p>No hay backups disponibles.</p>
      )}
    </div>
  );
};

export default BackupList;