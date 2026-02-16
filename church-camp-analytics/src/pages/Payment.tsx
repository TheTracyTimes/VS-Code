import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Payment.css';

const Payment: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { paymentOption } = location.state || { paymentOption: 'CashApp' };

  const handleBackHome = () => {
    navigate('/');
  };

  return (
    <div className="payment-page">
      <header className="payment-header">
        <div className="header-content">
          <h1>✅ Inscription Réussie!</h1>
          <p className="tagline">Merci pour votre inscription au camp</p>
        </div>
      </header>

      <main className="payment-main">
        <div className="success-card">
          <div className="success-icon">🎉</div>
          <h2>Votre inscription a été soumise avec succès!</h2>
          <p>Vous recevrez un email de confirmation sous peu.</p>
        </div>

        <div className="payment-info-card">
          <h3>💳 Information de Paiement</h3>
          <p className="payment-instruction">
            Veuillez compléter votre paiement via la méthode sélectionnée:
          </p>

          <div className="payment-method-selected">
            <strong>Méthode choisie:</strong> {paymentOption}
          </div>

          {paymentOption === 'CashApp' && (
            <div className="payment-details">
              <h4>CashApp</h4>
              <p className="payment-username">$ChurchCampPayment</p>
              <a
                href="https://cash.app/$ChurchCampPayment"
                target="_blank"
                rel="noopener noreferrer"
                className="payment-link-button"
              >
                Ouvrir CashApp
              </a>
              <p className="payment-note">
                Note: Veuillez inclure votre nom complet dans la note de paiement
              </p>
            </div>
          )}

          {paymentOption === 'Zelle' && (
            <div className="payment-details">
              <h4>Zelle</h4>
              <p className="payment-email">churchcamp@assemblee-laval.org</p>
              <p className="payment-instruction-text">
                Utilisez cette adresse email dans votre application Zelle pour envoyer le paiement
              </p>
              <p className="payment-note">
                Note: Veuillez inclure votre nom complet dans la note de paiement
              </p>
            </div>
          )}

          {paymentOption === 'Check' && (
            <div className="payment-details">
              <h4>Chèque</h4>
              <p className="payment-instruction-text">
                <strong>Libeller le chèque à l'ordre de:</strong><br />
                Assemblée Évangélique de Laval - Camp Ministry
              </p>
              <p className="payment-instruction-text">
                <strong>Apporter ou envoyer à:</strong><br />
                Assemblée Évangélique de Laval<br />
                123 Rue Example<br />
                Laval, QC H7X 1X1
              </p>
              <p className="payment-note">
                Note: Veuillez écrire votre nom complet au dos du chèque
              </p>
            </div>
          )}

          <div className="payment-amount-section">
            <h4>Montant du Camp</h4>
            <p className="amount-info">
              Le coût total du camp est de <strong>$XXX</strong> par personne.<br />
              (Le montant exact sera confirmé dans votre email de confirmation)
            </p>
          </div>
        </div>

        <div className="action-buttons">
          <button onClick={handleBackHome} className="back-home-button">
            Retour à l'accueil
          </button>
        </div>

        <div className="contact-info">
          <h4>Questions?</h4>
          <p>Si vous avez des questions concernant votre inscription ou le paiement:</p>
          <p>
            📧 Email: contact@assemblee-laval.org<br />
            📞 Téléphone: (555) 123-4567
          </p>
        </div>
      </main>

      <footer className="payment-footer">
        <p>© 2026 Assemblée Évangélique de Laval</p>
      </footer>
    </div>
  );
};

export default Payment;
