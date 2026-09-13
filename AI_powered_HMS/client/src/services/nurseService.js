import api from './api';

export const nurseService = {
  getDashboard: async () => {
    const res = await api.get('/nurse/dashboard');
    return res.data;
  },

  getPatients: async () => {
    const res = await api.get('/nurse/patients');
    return res.data;
  },

  recordVitals: async (vitalsData) => {
    const res = await api.post('/vitals', vitalsData);
    return res.data;
  },

  getVitalsHistory: async (patientId) => {
    const res = await api.get(`/vitals/${patientId}`);
    return res.data;
  },

  updateDuty: async (dutyData) => {
    const res = await api.post('/nurse/duty', dutyData);
    return res.data;
  },

  getDuty: async () => {
    const res = await api.get('/nurse/duty');
    return res.data;
  }
};
