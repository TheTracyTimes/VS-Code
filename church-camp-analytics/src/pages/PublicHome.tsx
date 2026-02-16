import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RegistrationForm from '../components/RegistrationForm';
import DoveAnimation from '../components/DoveAnimation';
import { submitRegistration } from '../api';
import type { Registration } from '../types';
import './PublicHome.css';

const PublicHome: React.FC = () => {
  const navigate = useNavigate();
  const [showDove, setShowDove] = useState(() => {
    const hasVisited = localStorage.getItem('hasVisitedCampAnalytics');
    return !hasVisited;
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleDoveComplete = () => {
    setShowDove(false);
    localStorage.setItem('hasVisitedCampAnalytics', 'true');
  };

  const handleSubmit = async (data: Omit<Registration, 'id' | 'timestamp'>) => {
    setIsSubmitting(true);
    setError('');

    try {
      await submitRegistration(data);
      // Redirect to payment page with registration data
      navigate('/payment', { state: { paymentOption: data.paymentOption } });
    } catch (err) {
      console.error('Registration error:', err);
      setError('Failed to submit registration. Please try again.');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="public-home">
      {showDove && <DoveAnimation onComplete={handleDoveComplete} />}

      <header className="public-header">
        <div className="header-content">
          <h1>⛺ Inscription au Camp de l'Église</h1>
          <p className="tagline">Assemblée Évangélique de Laval</p>
        </div>
      </header>

      <main className="public-main">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {isSubmitting ? (
          <div className="submitting-message">
            <div className="loader"></div>
            <p>Envoi de votre inscription...</p>
          </div>
        ) : (
          <RegistrationForm onSubmit={handleSubmit} />
        )}
      </main>

      <footer className="public-footer">
        <p>© 2026 Assemblée Évangélique de Laval</p>
        <p>Pour questions: contact@assemblee-laval.org</p>
      </footer>
    </div>
  );
};

export default PublicHome;
