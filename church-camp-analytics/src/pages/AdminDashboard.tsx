import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Dashboard from '../components/Dashboard';
import { getAnalytics, getAllRegistrations, exportRegistrationsCSV } from '../api';
import type { AnalyticsData, Registration } from '../types';
import './AdminDashboard.css';

const AdminDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [registrations, setRegistrations] = useState<Registration[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setIsLoading(true);
    setError('');

    try {
      const [analyticsData, regsData] = await Promise.all([
        getAnalytics(),
        getAllRegistrations(),
      ]);

      setAnalytics(analyticsData);
      setRegistrations(regsData);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Erreur lors du chargement des données. Veuillez vous reconnecter.');
      // If unauthorized, logout and redirect
      setTimeout(() => {
        logout();
        navigate('/admin');
      }, 2000);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/admin');
  };

  const handleExportCSV = () => {
    exportRegistrationsCSV(registrations);
  };

  const handleExportJSON = () => {
    const dataStr = JSON.stringify(registrations, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `camp-registrations-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  if (isLoading) {
    return (
      <div className="admin-dashboard-page">
        <div className="loading-container">
          <div className="loader"></div>
          <p>Chargement du tableau de bord...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard-page">
        <div className="error-container">
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard-page">
      <header className="admin-header">
        <div className="header-content">
          <div>
            <h1>📊 Tableau de Bord Administrateur</h1>
            <p className="tagline">Gestion des inscriptions au camp</p>
          </div>
          <button onClick={handleLogout} className="logout-button">
            Déconnexion
          </button>
        </div>
      </header>

      <main className="admin-main">
        <div className="admin-actions">
          <button onClick={fetchData} className="action-btn refresh-btn">
            🔄 Actualiser
          </button>
          <button onClick={handleExportJSON} className="action-btn">
            💾 Exporter JSON
          </button>
          <button onClick={handleExportCSV} className="action-btn">
            📄 Exporter CSV
          </button>
        </div>

        {analytics && <Dashboard analytics={analytics} />}

        {analytics && analytics.totalRegistrations === 0 && (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <h2>Aucune inscription pour le moment</h2>
            <p>Les inscriptions apparaîtront ici une fois que les participants auront soumis le formulaire.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default AdminDashboard;
