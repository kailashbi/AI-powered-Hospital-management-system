import api from './api';

export const patientService = {
  getDashboard: async () => {
    const res = await api.get('/patient/dashboard');
    return res.data;
  },

  getAppointments: async () => {
    const res = await api.get('/patient/appointments');
    return res.data;
  },

  bookAppointment: async (appointmentData) => {
    const res = await api.post('/patient/appointments', appointmentData);
    return res.data;
  },

  getMedicalRecords: async () => {
    const res = await api.get('/patient/medical-records');
    return res.data;
  },

  getPredictions: async () => {
    const res = await api.get('/patient/predictions');
    return res.data;
  },

  getProfile: async () => {
    const res = await api.get('/patient/profile');
    return res.data;
  },

  updateProfile: async (profileData) => {
    const res = await api.put('/patient/profile', profileData);
    return res.data;
  },

  getVitals: async () => {
    const res = await api.get('/patient/vitals');
    return res.data;
  }
};
