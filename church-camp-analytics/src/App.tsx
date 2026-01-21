import { useState, useEffect } from 'react';
import RegistrationForm from './components/RegistrationForm';
import Dashboard from './components/Dashboard';
import type { Registration } from './types';
import { calculateAnalytics, generateSampleData } from './utils/analytics';
import './App.css';

function App() {
  const [registrations, setRegistrations] = useState<Registration[]>([]);
  const [view, setView] = useState<'form' | 'dashboard'>('dashboard');
  const [showNotification, setShowNotification] = useState(false);

  // Load registrations from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('campRegistrations');
    if (saved) {
      const parsed = JSON.parse(saved);
      // Convert timestamp strings back to Date objects
      const withDates = parsed.map((r: Registration) => ({
        ...r,
        timestamp: new Date(r.timestamp),
      }));
      setRegistrations(withDates);
    } else {
      // Load sample data on first visit
      const sample = generateSampleData();
      setRegistrations(sample);
      localStorage.setItem('campRegistrations', JSON.stringify(sample));
    }
  }, []);

  // Save to localStorage whenever registrations change
  useEffect(() => {
    if (registrations.length > 0) {
      localStorage.setItem('campRegistrations', JSON.stringify(registrations));
    }
  }, [registrations]);

  const handleNewRegistration = (regData: Omit<Registration, 'id' | 'timestamp'>) => {
    const newRegistration: Registration = {
      ...regData,
      id: `reg-${Date.now()}`,
      timestamp: new Date(),
    };

    setRegistrations([...registrations, newRegistration]);
    setView('dashboard');
    showSuccessNotification();
  };

  const showSuccessNotification = () => {
    setShowNotification(true);
    setTimeout(() => setShowNotification(false), 3000);
  };

  const loadSampleData = () => {
    const sample = generateSampleData();
    setRegistrations(sample);
    localStorage.setItem('campRegistrations', JSON.stringify(sample));
  };

  const clearAllData = () => {
    if (window.confirm('Are you sure you want to clear all registration data? This cannot be undone.')) {
      setRegistrations([]);
      localStorage.removeItem('campRegistrations');
    }
  };

  const exportToJSON = () => {
    const dataStr = JSON.stringify(registrations, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `camp-registrations-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const exportToCSV = () => {
    if (registrations.length === 0) {
      alert('No data to export');
      return;
    }

    const headers = [
      'ID',
      'Timestamp',
      'First Name',
      'Last Name',
      'Age',
      'Email',
      'Phone',
      'Country',
      'State/Province',
      'City',
      'Previously Attended',
      'Times Attended',
      'Heard About Camp',
      'Interests',
      'Dietary Restrictions',
      'T-Shirt Size',
      'Transportation Needed',
      'Transportation Method',
      'Accommodation Type',
      'Financial Aid Needed',
      'Estimated Budget',
      'Emergency Contact Name',
      'Emergency Contact Phone',
      'Emergency Contact Relation',
      'Special Needs',
      'Comments',
    ];

    const rows = registrations.map(r => [
      r.id,
      new Date(r.timestamp).toISOString(),
      r.firstName,
      r.lastName,
      r.age,
      r.email,
      r.phone,
      r.country,
      r.stateProvince,
      r.city,
      r.previouslyAttended,
      r.timesAttended,
      r.heardAboutCamp,
      r.interests.join('; '),
      r.dietaryRestrictions.join('; '),
      r.tShirtSize,
      r.transportationNeeded,
      r.transportationMethod,
      r.accommodationType,
      r.financialAidNeeded,
      r.estimatedBudget,
      r.emergencyContactName,
      r.emergencyContactPhone,
      r.emergencyContactRelation,
      r.specialNeeds,
      r.comments,
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `camp-registrations-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const analytics = calculateAnalytics(registrations);

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>⛺ Church Camp Analytics</h1>
          <p className="tagline">Interactive Registration & Data Visualization Platform</p>
        </div>

        <nav className="app-nav">
          <button
            className={`nav-button ${view === 'dashboard' ? 'active' : ''}`}
            onClick={() => setView('dashboard')}
          >
            📊 Dashboard
          </button>
          <button
            className={`nav-button ${view === 'form' ? 'active' : ''}`}
            onClick={() => setView('form')}
          >
            📝 New Registration
          </button>
        </nav>
      </header>

      {/* Success Notification */}
      {showNotification && (
        <div className="notification success">
          ✓ Registration submitted successfully!
        </div>
      )}

      {/* Main Content */}
      <main className="app-main">
        {view === 'dashboard' ? (
          <>
            <div className="dashboard-actions">
              <button onClick={loadSampleData} className="action-button secondary">
                🔄 Load Sample Data
              </button>
              <button onClick={exportToJSON} className="action-button secondary">
                💾 Export JSON
              </button>
              <button onClick={exportToCSV} className="action-button secondary">
                📄 Export CSV
              </button>
              <button onClick={clearAllData} className="action-button danger">
                🗑️ Clear All Data
              </button>
            </div>
            <Dashboard analytics={analytics} />
          </>
        ) : (
          <RegistrationForm onSubmit={handleNewRegistration} />
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>
          Built with React + TypeScript + Recharts | Designed for learning data analytics and UI/UX design
        </p>
        <p className="footer-note">
          This interactive platform helps visualize registration data in real-time for better camp planning and cost analysis.
        </p>
      </footer>
    </div>
  );
}

export default App;
