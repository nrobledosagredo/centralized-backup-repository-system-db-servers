import React from 'react';

const BackupItem = ({ backup, onDelete, size, firstInGroup, groupLength }) => {
  const handleClick = () => {
    onDelete(backup.name, backup.owner);
  };

  const formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  };

  const getFormattedDate = (backupName) => {
    const dateRegex = /(\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2})/;
    const dateString = backupName.match(dateRegex)[1];
    const date = new Date(
      parseInt(dateString.slice(0, 4), 10),
      parseInt(dateString.slice(4, 6), 10) - 1,
      parseInt(dateString.slice(6, 8), 10),
      parseInt(dateString.slice(9, 11), 10),
      parseInt(dateString.slice(11, 13), 10),
      parseInt(dateString.slice(13, 15), 10)
    );
    return date.toLocaleString();
  };

  return (
    <tr>
      <td>{backup.name}</td>
      <td>{getFormattedDate(backup.name)}</td>
      <td>{formatBytes(size)}</td>
      {firstInGroup ? (
        <td rowSpan={groupLength} style={{ verticalAlign: 'middle' }}>
          {backup.owner}
        </td>
      ) : null}
      <td>
        <button onClick={handleClick}>Eliminar backup</button>
      </td>
    </tr>
  );
};

export default BackupItem;