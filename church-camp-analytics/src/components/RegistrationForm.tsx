import React, { useState } from 'react';
import type { Registration } from '../types';
import './RegistrationForm.css';

interface RegistrationFormProps {
  onSubmit: (registration: Omit<Registration, 'id' | 'timestamp'>) => void;
}

const RegistrationForm: React.FC<RegistrationFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    gender: '',
    age: 18,
    chaperoneName: '',
    phone: '',
    email: '',
    nationality: '',
    assembly: '',
    transportation: '',
    allergies: '',
    emergencyContactName: '',
    emergencyContactPhone: '',
    comments: '',
    concerns: '',
    questions: '',
    paymentOption: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;

    if (type === 'number') {
      setFormData(prev => ({ ...prev, [name]: parseInt(value) || 0 }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate chaperone requirement
    if (formData.age < 18 && !formData.chaperoneName.trim()) {
      alert('A chaperone name is required for attendees under 18 years old.');
      return;
    }

    onSubmit(formData);

    // Reset form
    setFormData({
      firstName: '',
      lastName: '',
      gender: '',
      age: 18,
      chaperoneName: '',
      phone: '',
      email: '',
      nationality: '',
      assembly: '',
      transportation: '',
      allergies: '',
      emergencyContactName: '',
      emergencyContactPhone: '',
      comments: '',
      concerns: '',
      questions: '',
      paymentOption: '',
    });
  };

  const assemblies = [
    'Assemblée Évangélique de Laval (Pastor Exavier Noel & Pastor Rosage Beauzil)',
    'Assemblée Évangélique de Montreal (Pastor David Paul)',
    'Tabernacle Evangelique Mahanaim (Pastor Gesner Dorzin)',
    'Gospel Assembly of the Kingdom of Peace (Pastor Ancelot Joseph)',
    'Assemblée Évangélique (Pastor Jean Bazelais)',
    'Eglise de la Nouvelle Alliance (Pastor Vitalerme Dorestant)',
    'Eglise du Corps de Christ (Pastor Wilner Dumond)',
    'Sarasota Gospel Temple (Pastor Edwige Achile)',
    'Christian Family Gospel Assembly (Pastor Kennedy Demosthenes)',
    'Ansonia Gospel Assembly (Pastor Jowel Guerrier)',
    'Gospel Assembly Church (Pastor Noisin Raphael)',
    'Boston Gospel Congregation (Pastor Guy Mauristhene)',
    'First Church of the Latter Rain (Pastor Wilson Douce)',
    'God of Mercy Church (Pastor Hogarth Louis)',
    'First Church of Brooklyn (Pastor Jean Michaud Derissant)',
    'Christian Church of the Latter Rain (Pastor Jean Raymond Pharaud)',
    'Gospel Church of Hope (Pastor Augustin Dalusma)',
    'Other',
  ];

  return (
    <form onSubmit={handleSubmit} className="registration-form">
      <h2>Church Camp Registration Form</h2>
      <p className="form-description">Please complete all required fields (*) to register for our church camp.</p>

      {/* Personal Information */}
      <section className="form-section">
        <h3>Personal Information</h3>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="firstName">1. First Name *</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="lastName">2. Last Name *</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="gender">3. Gender *</label>
            <select
              id="gender"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              required
            >
              <option value="">Select gender</option>
              <option value="Female">Female</option>
              <option value="Male">Male</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="age">4. Age (13-40) *</label>
            <input
              type="number"
              id="age"
              name="age"
              min="13"
              max="40"
              value={formData.age}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        {/* Conditional Chaperone Field */}
        {formData.age < 18 && (
          <div className="form-group conditional-field">
            <label htmlFor="chaperoneName">5. Chaperone Name (Required for under 18) *</label>
            <input
              type="text"
              id="chaperoneName"
              name="chaperoneName"
              value={formData.chaperoneName}
              onChange={handleChange}
              required={formData.age < 18}
              placeholder="Required for attendees under 18"
            />
            <small className="helper-text">A chaperone is required for all attendees under 18 years old</small>
          </div>
        )}

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="phone">6. Phone Number *</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+1-555-1234"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">7. Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="nationality">8. Nationality *</label>
          <select
            id="nationality"
            name="nationality"
            value={formData.nationality}
            onChange={handleChange}
            required
          >
            <option value="">Select nationality</option>
            <option value="French">French</option>
            <option value="Canadian">Canadian</option>
            <option value="American">American</option>
          </select>
        </div>
      </section>

      {/* Church Information */}
      <section className="form-section">
        <h3>Church Information</h3>

        <div className="form-group">
          <label htmlFor="assembly">9. Assembly *</label>
          <select
            id="assembly"
            name="assembly"
            value={formData.assembly}
            onChange={handleChange}
            required
          >
            <option value="">Select your assembly</option>
            {assemblies.map(assembly => (
              <option key={assembly} value={assembly}>
                {assembly}
              </option>
            ))}
          </select>
        </div>
      </section>

      {/* Transportation & Logistics */}
      <section className="form-section">
        <h3>Transportation & Health</h3>

        <div className="form-group">
          <label htmlFor="transportation">10. Transportation *</label>
          <select
            id="transportation"
            name="transportation"
            value={formData.transportation}
            onChange={handleChange}
            required
          >
            <option value="">Select transportation option</option>
            <option value="Personal car">Personal car</option>
            <option value="Church bus">Church bus</option>
            <option value="Carpooling">Carpooling</option>
            <option value="Public transit">Public transit</option>
            <option value="Need ride">Need ride</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="allergies">11. Allergies</label>
          <input
            type="text"
            id="allergies"
            name="allergies"
            value={formData.allergies}
            onChange={handleChange}
            placeholder="e.g., Peanuts, Shellfish, Lactose, or 'None'"
          />
          <small className="helper-text">Please list any allergies or dietary restrictions</small>
        </div>
      </section>

      {/* Emergency Contact */}
      <section className="form-section">
        <h3>Emergency Contact</h3>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="emergencyContactName">12. Emergency Contact Name *</label>
            <input
              type="text"
              id="emergencyContactName"
              name="emergencyContactName"
              value={formData.emergencyContactName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="emergencyContactPhone">Emergency Contact Phone *</label>
            <input
              type="tel"
              id="emergencyContactPhone"
              name="emergencyContactPhone"
              value={formData.emergencyContactPhone}
              onChange={handleChange}
              required
            />
          </div>
        </div>
      </section>

      {/* Additional Information */}
      <section className="form-section">
        <h3>Additional Information</h3>

        <div className="form-group">
          <label htmlFor="comments">13. Comments</label>
          <textarea
            id="comments"
            name="comments"
            value={formData.comments}
            onChange={handleChange}
            rows={3}
            placeholder="Any additional comments or information you'd like to share..."
          />
        </div>

        <div className="form-group">
          <label htmlFor="concerns">14. Concerns</label>
          <textarea
            id="concerns"
            name="concerns"
            value={formData.concerns}
            onChange={handleChange}
            rows={3}
            placeholder="Do you have any concerns we should be aware of?"
          />
        </div>

        <div className="form-group">
          <label htmlFor="questions">15. Questions</label>
          <textarea
            id="questions"
            name="questions"
            value={formData.questions}
            onChange={handleChange}
            rows={3}
            placeholder="Any questions about the camp?"
          />
        </div>
      </section>

      {/* Payment Information */}
      <section className="form-section payment-section">
        <h3>Payment Information</h3>

        <div className="form-group">
          <label htmlFor="paymentOption">16. Payment Option *</label>
          <select
            id="paymentOption"
            name="paymentOption"
            value={formData.paymentOption}
            onChange={handleChange}
            required
          >
            <option value="">Select payment method</option>
            <option value="CashApp">CashApp</option>
            <option value="Zelle">Zelle</option>
            <option value="Check">Check</option>
          </select>
        </div>

        {formData.paymentOption && (
          <div className="payment-info">
            <div className="info-box">
              <h4>📱 Payment Details</h4>
              {formData.paymentOption === 'CashApp' && (
                <div>
                  <p><strong>CashApp:</strong> $ChurchCampPayment</p>
                  <a href="https://cash.app/$ChurchCampPayment" target="_blank" rel="noopener noreferrer" className="payment-link">
                    Click here to pay via CashApp
                  </a>
                </div>
              )}
              {formData.paymentOption === 'Zelle' && (
                <div>
                  <p><strong>Zelle:</strong> churchcamp@example.com</p>
                  <p className="helper-text">Use this email to send payment via Zelle</p>
                </div>
              )}
              {formData.paymentOption === 'Check' && (
                <div>
                  <p><strong>Make checks payable to:</strong> Church Camp Ministry</p>
                  <p className="helper-text">Please bring your check to the church office or mail to the address provided in your confirmation email</p>
                </div>
              )}
            </div>
          </div>
        )}
      </section>

      <button type="submit" className="submit-button">Submit Registration</button>

      <p className="form-footer">
        After submitting, you will receive a confirmation email with additional details about the camp.
      </p>
    </form>
  );
};

export default RegistrationForm;
