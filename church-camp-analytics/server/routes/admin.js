const express = require('express');
const router = express.Router();
const Registration = require('../models/Registration');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

// Admin password (in production, this should be in environment variables)
const ADMIN_PASSWORD_HASH = process.env.ADMIN_PASSWORD_HASH || bcrypt.hashSync('admin123', 10);
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// Middleware to verify admin token
const verifyAdminToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.admin = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// POST /api/admin/login - Admin login
router.post('/login', async (req, res) => {
  try {
    const { password } = req.body;

    const isValid = await bcrypt.compare(password, ADMIN_PASSWORD_HASH);

    if (!isValid) {
      return res.status(401).json({ error: 'Invalid password' });
    }

    const token = jwt.sign(
      { role: 'admin', timestamp: Date.now() },
      JWT_SECRET,
      { expiresIn: '24h' }
    );

    res.json({
      success: true,
      token,
      expiresIn: 86400, // 24 hours in seconds
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET /api/admin/registrations - Get all registrations (protected)
router.get('/registrations', verifyAdminToken, async (req, res) => {
  try {
    const registrations = await Registration.find()
      .sort({ timestamp: -1 })
      .lean();

    res.json(registrations);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET /api/admin/analytics - Get calculated analytics (protected)
router.get('/analytics', verifyAdminToken, async (req, res) => {
  try {
    const registrations = await Registration.find().lean();

    // Calculate analytics
    const analytics = calculateAnalytics(registrations);

    res.json(analytics);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// DELETE /api/admin/registrations/:id - Delete registration (protected)
router.delete('/registrations/:id', verifyAdminToken, async (req, res) => {
  try {
    await Registration.findByIdAndDelete(req.params.id);
    res.json({ success: true, message: 'Registration deleted' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Helper function to calculate analytics
function calculateAnalytics(registrations) {
  if (registrations.length === 0) {
    return {
      totalRegistrations: 0,
      averageAge: 0,
      ageDistribution: {},
      genderDistribution: {},
      nationalityDistribution: {},
      assemblyDistribution: {},
      transportationStats: {},
      allergyStats: {},
      paymentOptionStats: {},
      registrationTimeline: [],
      minorsRequiringChaperone: 0,
    };
  }

  const totalRegistrations = registrations.length;
  const averageAge = registrations.reduce((sum, r) => sum + r.age, 0) / totalRegistrations;

  // Age distribution
  const ageDistribution = {};
  const ageRanges = ['13-17', '18-24', '25-30', '31-35', '36-40'];
  ageRanges.forEach(range => ageDistribution[range] = 0);

  registrations.forEach(r => {
    if (r.age >= 13 && r.age <= 17) ageDistribution['13-17']++;
    else if (r.age >= 18 && r.age <= 24) ageDistribution['18-24']++;
    else if (r.age >= 25 && r.age <= 30) ageDistribution['25-30']++;
    else if (r.age >= 31 && r.age <= 35) ageDistribution['31-35']++;
    else if (r.age >= 36 && r.age <= 40) ageDistribution['36-40']++;
  });

  // Other distributions
  const genderDistribution = countOccurrences(registrations.map(r => r.gender));
  const nationalityDistribution = countOccurrences(registrations.map(r => r.nationality));
  const assemblyDistribution = countOccurrences(registrations.map(r => r.assembly));
  const transportationStats = countOccurrences(registrations.map(r => r.transportation).filter(t => t));

  // Allergies
  const allergyStats = {};
  const hasAllergies = registrations.filter(r => r.allergies && r.allergies.toLowerCase() !== 'none' && r.allergies.trim() !== '').length;
  const noAllergies = registrations.length - hasAllergies;
  if (hasAllergies > 0) allergyStats['Has Allergies'] = hasAllergies;
  if (noAllergies > 0) allergyStats['No Allergies'] = noAllergies;

  const paymentOptionStats = countOccurrences(registrations.map(r => r.paymentOption));

  // Registration timeline
  const timelineMap = new Map();
  registrations.forEach(r => {
    const date = new Date(r.timestamp).toISOString().split('T')[0];
    timelineMap.set(date, (timelineMap.get(date) || 0) + 1);
  });
  const registrationTimeline = Array.from(timelineMap.entries())
    .map(([date, count]) => ({ date, count }))
    .sort((a, b) => new Date(a.date) - new Date(b.date));

  const minorsRequiringChaperone = registrations.filter(r => r.age < 18).length;

  return {
    totalRegistrations,
    averageAge: Math.round(averageAge * 10) / 10,
    ageDistribution,
    genderDistribution,
    nationalityDistribution,
    assemblyDistribution,
    transportationStats,
    allergyStats,
    paymentOptionStats,
    registrationTimeline,
    minorsRequiringChaperone,
  };
}

function countOccurrences(items) {
  return items.reduce((acc, item) => {
    if (item) {
      acc[item] = (acc[item] || 0) + 1;
    }
    return acc;
  }, {});
}

module.exports = router;
