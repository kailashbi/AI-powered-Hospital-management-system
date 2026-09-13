import api from './api';

export const doctorService = {
  getDashboard: async () => {
    const res = await api.get('/doctor/dashboard');
    return res.data;
  },

  getPatients: async (search) => {
    const res = await api.get('/doctor/patients', { params: { search } });
    return res.data;
  },

  getPatientDetail: async (patientId) => {
    const res = await api.get(`/doctor/patients/${patientId}`);
    return res.data;
  },

  createMedicalRecord: async (recordData) => {
    const res = await api.post('/doctor/medical-records', recordData);
    return res.data;
  },

  sendNotification: async (alertData) => {
    const res = await api.post('/doctor/send-patient-notification', alertData);
    return res.data;
  },

  updateAppointmentStatus: async (apptId, status, notes) => {
    const res = await api.patch(`/appointments/${apptId}/status`, { status, doctor_notes: notes });
    return res.data;
  }
};
