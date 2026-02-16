import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { adminLogin } from '../api';
import './AdminLogin.css';

const AdminLogin: React.FC = () => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await adminLogin(password);
      login(response.token);
      navigate('/admin/dashboard');
    } catch (err) {
      setError('Mot de passe incorrect. Veuillez réessayer.');
      setPassword('');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="admin-login-page">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <h1>🔐 Connexion Administrateur</h1>
            <p>Tableau de bord des inscriptions au camp</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            {error && (
              <div className="error-alert">
                {error}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="password">Mot de passe</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Entrez le mot de passe administrateur"
                autoFocus
                disabled={isLoading}
              />
            </div>

            <button type="submit" className="login-button" disabled={isLoading}>
              {isLoading ? 'Connexion...' : 'Se connecter'}
            </button>
          </form>

          <div className="login-footer">
            <p>
              <a href="/">← Retour à la page d'inscription</a>
            </p>
          </div>
        </div>

        <div className="login-info">
          <p>💡 <strong>Mot de passe par défaut:</strong> admin123</p>
          <p className="security-note">
            ⚠️ Changez ce mot de passe dans les variables d'environnement
            pour la production
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
