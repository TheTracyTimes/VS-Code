import React, { useState } from 'react';
import { Registration } from '../types';
import './RegistrationForm.css';

interface RegistrationFormProps {
  onSubmit: (registration: Omit<Registration, 'id' | 'timestamp'>) => void;
}

const RegistrationForm: React.FC<RegistrationFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    age: 18,
    email: '',
    phone: '',
    country: '',
    stateProvince: '',
    city: '',
    previouslyAttended: false,
    timesAttended: 0,
    heardAboutCamp: '',
    interests: [] as string[],
    dietaryRestrictions: [] as string[],
    tShirtSize: '',
    transportationNeeded: false,
    transportationMethod: '',
    accommodationType: '',
    financialAidNeeded: false,
    estimatedBudget: '',
    emergencyContactName: '',
    emergencyContactPhone: '',
    emergencyContactRelation: '',
    specialNeeds: '',
    comments: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;

    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else if (type === 'number') {
      setFormData(prev => ({ ...prev, [name]: parseInt(value) || 0 }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleMultiSelect = (value: string, field: 'interests' | 'dietaryRestrictions') => {
    setFormData(prev => {
      const currentValues = prev[field];
      const newValues = currentValues.includes(value)
        ? currentValues.filter(v => v !== value)
        : [...currentValues, value];
      return { ...prev, [field]: newValues };
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    // Reset form
    setFormData({
      firstName: '',
      lastName: '',
      age: 18,
      email: '',
      phone: '',
      country: '',
      stateProvince: '',
      city: '',
      previouslyAttended: false,
      timesAttended: 0,
      heardAboutCamp: '',
      interests: [],
      dietaryRestrictions: [],
      tShirtSize: '',
      transportationNeeded: false,
      transportationMethod: '',
      accommodationType: '',
      financialAidNeeded: false,
      estimatedBudget: '',
      emergencyContactName: '',
      emergencyContactPhone: '',
      emergencyContactRelation: '',
      specialNeeds: '',
      comments: '',
    });
  };

  const interestOptions = ['Worship', 'Bible study', 'Sports', 'Arts & crafts', 'Music', 'Community service', 'Leadership'];
  const dietaryOptions = ['None', 'Vegetarian', 'Vegan', 'Gluten-free', 'Halal', 'Kosher', 'Nut allergy', 'Lactose intolerant'];

  return (
    <form onSubmit={handleSubmit} className="registration-form">
      <h2>Church Camp Registration Form</h2>
      <p className="form-description">Complete this form to register for our upcoming church camp. All fields marked with * are required.</p>

      {/* Personal Information */}
      <section className="form-section">
        <h3>Personal Information</h3>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="firstName">First Name *</label>
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
            <label htmlFor="lastName">Last Name *</label>
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
            <label htmlFor="age">Age (13-40) *</label>
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
          <div className="form-group">
            <label htmlFor="email">Email *</label>
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
          <label htmlFor="phone">Phone Number *</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            required
          />
        </div>
      </section>

      {/* Geographic Information */}
      <section className="form-section">
        <h3>Location Information</h3>
        <div className="form-group">
          <label htmlFor="country">Country *</label>
          <select
            id="country"
            name="country"
            value={formData.country}
            onChange={handleChange}
            required
          >
            <option value="">Select a country</option>
            <option value="Canada">Canada</option>
            <option value="United States">United States</option>
            <option value="Haiti">Haiti</option>
            <option value="France">France</option>
            <option value="Congo">Democratic Republic of Congo</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="stateProvince">State/Province *</label>
            <input
              type="text"
              id="stateProvince"
              name="stateProvince"
              value={formData.stateProvince}
              onChange={handleChange}
              placeholder="e.g., Quebec, Ontario, New York"
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="city">City *</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleChange}
              required
            />
          </div>
        </div>
      </section>

      {/* Camp Experience */}
      <section className="form-section">
        <h3>Camp Experience</h3>
        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              name="previouslyAttended"
              checked={formData.previouslyAttended}
              onChange={handleChange}
            />
            I have attended this camp before
          </label>
        </div>

        {formData.previouslyAttended && (
          <div className="form-group">
            <label htmlFor="timesAttended">How many times?</label>
            <input
              type="number"
              id="timesAttended"
              name="timesAttended"
              min="0"
              value={formData.timesAttended}
              onChange={handleChange}
            />
          </div>
        )}

        <div className="form-group">
          <label htmlFor="heardAboutCamp">How did you hear about this camp? *</label>
          <select
            id="heardAboutCamp"
            name="heardAboutCamp"
            value={formData.heardAboutCamp}
            onChange={handleChange}
            required
          >
            <option value="">Select an option</option>
            <option value="Church announcement">Church announcement</option>
            <option value="Friend">Friend</option>
            <option value="Social media">Social media</option>
            <option value="Website">Website</option>
            <option value="Previous attendee">Previous attendee</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </section>

      {/* Program Interests */}
      <section className="form-section">
        <h3>Program Interests</h3>
        <p className="helper-text">Select all activities you're interested in:</p>
        <div className="checkbox-grid">
          {interestOptions.map(interest => (
            <label key={interest} className="checkbox-label">
              <input
                type="checkbox"
                checked={formData.interests.includes(interest)}
                onChange={() => handleMultiSelect(interest, 'interests')}
              />
              {interest}
            </label>
          ))}
        </div>
      </section>

      {/* Dietary & Logistics */}
      <section className="form-section">
        <h3>Dietary Restrictions</h3>
        <div className="checkbox-grid">
          {dietaryOptions.map(dietary => (
            <label key={dietary} className="checkbox-label">
              <input
                type="checkbox"
                checked={formData.dietaryRestrictions.includes(dietary)}
                onChange={() => handleMultiSelect(dietary, 'dietaryRestrictions')}
              />
              {dietary}
            </label>
          ))}
        </div>

        <div className="form-group">
          <label htmlFor="tShirtSize">T-Shirt Size *</label>
          <select
            id="tShirtSize"
            name="tShirtSize"
            value={formData.tShirtSize}
            onChange={handleChange}
            required
          >
            <option value="">Select a size</option>
            <option value="XS">XS</option>
            <option value="S">S</option>
            <option value="M">M</option>
            <option value="L">L</option>
            <option value="XL">XL</option>
            <option value="XXL">XXL</option>
          </select>
        </div>
      </section>

      {/* Transportation & Accommodation */}
      <section className="form-section">
        <h3>Transportation & Accommodation</h3>
        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              name="transportationNeeded"
              checked={formData.transportationNeeded}
              onChange={handleChange}
            />
            I need transportation assistance
          </label>
        </div>

        {formData.transportationNeeded && (
          <div className="form-group">
            <label htmlFor="transportationMethod">Preferred transportation method</label>
            <select
              id="transportationMethod"
              name="transportationMethod"
              value={formData.transportationMethod}
              onChange={handleChange}
            >
              <option value="">Select an option</option>
              <option value="Church bus">Church bus</option>
              <option value="Carpooling">Carpooling</option>
              <option value="Public transit">Public transit</option>
              <option value="Personal car">Personal car</option>
            </select>
          </div>
        )}

        <div className="form-group">
          <label htmlFor="accommodationType">Accommodation preference *</label>
          <select
            id="accommodationType"
            name="accommodationType"
            value={formData.accommodationType}
            onChange={handleChange}
            required
          >
            <option value="">Select an option</option>
            <option value="Shared cabin">Shared cabin</option>
            <option value="Private room">Private room</option>
            <option value="Tent">Tent</option>
            <option value="RV">RV</option>
          </select>
        </div>
      </section>

      {/* Financial Information */}
      <section className="form-section">
        <h3>Financial Information</h3>
        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              name="financialAidNeeded"
              checked={formData.financialAidNeeded}
              onChange={handleChange}
            />
            I am interested in financial aid
          </label>
        </div>

        <div className="form-group">
          <label htmlFor="estimatedBudget">Estimated budget for camp *</label>
          <select
            id="estimatedBudget"
            name="estimatedBudget"
            value={formData.estimatedBudget}
            onChange={handleChange}
            required
          >
            <option value="">Select a range</option>
            <option value="$0-$100">$0-$100</option>
            <option value="$100-$200">$100-$200</option>
            <option value="$200-$300">$200-$300</option>
            <option value="$300-$500">$300-$500</option>
            <option value="$500+">$500+</option>
          </select>
        </div>
      </section>

      {/* Emergency Contact */}
      <section className="form-section">
        <h3>Emergency Contact</h3>
        <div className="form-group">
          <label htmlFor="emergencyContactName">Emergency contact name *</label>
          <input
            type="text"
            id="emergencyContactName"
            name="emergencyContactName"
            value={formData.emergencyContactName}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="emergencyContactPhone">Emergency contact phone *</label>
            <input
              type="tel"
              id="emergencyContactPhone"
              name="emergencyContactPhone"
              value={formData.emergencyContactPhone}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="emergencyContactRelation">Relationship *</label>
            <select
              id="emergencyContactRelation"
              name="emergencyContactRelation"
              value={formData.emergencyContactRelation}
              onChange={handleChange}
              required
            >
              <option value="">Select relationship</option>
              <option value="Parent">Parent</option>
              <option value="Spouse">Spouse</option>
              <option value="Sibling">Sibling</option>
              <option value="Friend">Friend</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>
      </section>

      {/* Additional Information */}
      <section className="form-section">
        <h3>Additional Information</h3>
        <div className="form-group">
          <label htmlFor="specialNeeds">Special needs or medical conditions</label>
          <textarea
            id="specialNeeds"
            name="specialNeeds"
            value={formData.specialNeeds}
            onChange={handleChange}
            rows={3}
            placeholder="Please list any special needs or medical conditions we should be aware of"
          />
        </div>

        <div className="form-group">
          <label htmlFor="comments">Additional comments or questions</label>
          <textarea
            id="comments"
            name="comments"
            value={formData.comments}
            onChange={handleChange}
            rows={3}
            placeholder="Any additional information you'd like to share"
          />
        </div>
      </section>

      <button type="submit" className="submit-button">Submit Registration</button>
    </form>
  );
};

export default RegistrationForm;
