import api from './api';

export const nurseService = {
  getDashboard: async () => {
    const res = await api.get('/nurse/dashboard');
    return res.data;
  },

  recordVitals: async (vitalsData) => {
    const res = await api.post('/nurse/vitals', vitalsData);
    return res.data;
  },

  updateDuty: async (dutyData) => {
    const res = await api.patch('/nurse/update-duty', dutyData);
    return res.data;
  }
};

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

  getVitals: async () => {
    const res = await api.get('/patient/vitals');
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

  getNotifications: async () => {
    const res = await api.get('/notifications');
    return res.data;
  },

  markNotificationRead: async (notifId) => {
    const res = await api.patch(`/notifications/${notifId}/read`);
    return res.data;
  }
};

export const predictionService = {
  predict: async (patientId, diseaseType, features) => {
    const res = await api.post('/predictions/predict', {
      patient_id: patientId,
      disease_type: diseaseType,
      features: features
    });
    return res.data;
  },

  getHistory: async (patientId) => {
    const res = await api.get(`/predictions/history/${patientId}`);
    return res.data;
  },

  getMetrics: async () => {
    const res = await api.get('/predictions/metrics');
    return res.data;
  },

  updateFeedback: async (predId, feedback) => {
    const res = await api.patch(`/predictions/${predId}/feedback`, { feedback });
    return res.data;
  }
};
