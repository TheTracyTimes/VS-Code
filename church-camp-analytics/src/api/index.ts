import axios from 'axios';
import type { Registration, AnalyticsData } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('adminToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Public API
export const submitRegistration = async (data: Omit<Registration, 'id' | 'timestamp'>) => {
  const response = await api.post('/registrations', data);
  return response.data;
};

export const getRegistrationCount = async () => {
  const response = await api.get('/registrations/count');
  return response.data.count;
};

// Admin API
export const adminLogin = async (password: string) => {
  const response = await api.post('/admin/login', { password });
  return response.data;
};

export const getAllRegistrations = async (): Promise<Registration[]> => {
  const response = await api.get('/admin/registrations');
  return response.data;
};

export const getAnalytics = async (): Promise<AnalyticsData> => {
  const response = await api.get('/admin/analytics');
  return response.data;
};

export const deleteRegistration = async (id: string) => {
  const response = await api.delete(`/admin/registrations/${id}`);
  return response.data;
};

export const exportRegistrationsCSV = (registrations: Registration[]) => {
  const headers = [
    'ID',
    'Timestamp',
    'First Name',
    'Last Name',
    'Gender',
    'Age',
    'Chaperone Name',
    'Phone',
    'Email',
    'Nationality',
    'Assembly',
    'Transportation',
    'Allergies',
    'Emergency Contact Name',
    'Emergency Contact Phone',
    'Comments',
    'Concerns',
    'Questions',
    'Payment Option',
  ];

  const rows = registrations.map(r => [
    r.id,
    new Date(r.timestamp).toISOString(),
    r.firstName,
    r.lastName,
    r.gender,
    r.age,
    r.chaperoneName,
    r.phone,
    r.email,
    r.nationality,
    r.assembly,
    r.transportation,
    r.allergies,
    r.emergencyContactName,
    r.emergencyContactPhone,
    r.comments,
    r.concerns,
    r.questions,
    r.paymentOption,
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
