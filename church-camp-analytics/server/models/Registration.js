const mongoose = require('mongoose');

const registrationSchema = new mongoose.Schema({
  // Personal Information
  firstName: { type: String, required: true },
  lastName: { type: String, required: true },
  gender: { type: String, required: true },
  age: { type: Number, required: true },
  chaperoneName: { type: String, default: '' },
  phone: { type: String, required: true },
  email: { type: String, required: true },
  nationality: { type: String, required: true },

  // Church Information
  assembly: { type: String, required: true },

  // Transportation & Logistics
  transportation: { type: String, required: true },
  allergies: { type: String, default: '' },

  // Emergency Contact
  emergencyContactName: { type: String, required: true },
  emergencyContactPhone: { type: String, required: true },

  // Additional Information
  comments: { type: String, default: '' },
  concerns: { type: String, default: '' },
  questions: { type: String, default: '' },

  // Payment
  paymentOption: { type: String, required: true },
  paymentCompleted: { type: Boolean, default: false },

  // Metadata
  timestamp: { type: Date, default: Date.now },
  ipAddress: String,
}, {
  timestamps: true
});

module.exports = mongoose.model('Registration', registrationSchema);
