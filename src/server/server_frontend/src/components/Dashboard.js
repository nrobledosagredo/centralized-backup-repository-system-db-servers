import React, { useState, useEffect } from 'react';
import axios from 'axios';
import BackupList from './BackupList';

const Dashboard = () => {
  // Define el estado de los respaldos y establece el valor inicial como un arreglo vacío
  const [backups, setBackups] = useState([]);

  // Utiliza useEffect para obtener la lista de respaldos al cargar el componente
  useEffect(() => {
    const fetchData = async () => {
      // Realiza una solicitud GET para obtener la lista de respaldos desde la API
      const result = await axios.get('http://localhost:5000/api/get_backups');
      
      // Actualiza el estado de los respaldos con los datos recibidos
      setBackups(result.data.backups);
    };

    // Llama a la función fetchData para obtener los respaldos
    fetchData();
  }, []);

  return (
    <div className="dashboard">
      <h1>Backup centralizado</h1>
      {/* Muestra la lista de respaldos utilizando el componente BackupList */}
      <BackupList backups={backups} />
    </div>
  );
};

export default Dashboard;