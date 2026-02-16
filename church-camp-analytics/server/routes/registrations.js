const express = require('express');
const router = express.Router();
const Registration = require('../models/Registration');

// POST /api/registrations - Submit new registration
router.post('/', async (req, res) => {
  try {
    const registrationData = {
      ...req.body,
      ipAddress: req.ip,
      timestamp: new Date(),
    };

    const registration = new Registration(registrationData);
    await registration.save();

    res.status(201).json({
      success: true,
      message: 'Registration submitted successfully',
      registrationId: registration._id,
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to submit registration',
      error: error.message,
    });
  }
});

// GET /api/registrations/count - Get total count (public)
router.get('/count', async (req, res) => {
  try {
    const count = await Registration.countDocuments();
    res.json({ count });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
