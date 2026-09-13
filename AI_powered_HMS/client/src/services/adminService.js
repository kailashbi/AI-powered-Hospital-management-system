import api from './api';

export const adminService = {
  getStats: async () => {
    const res = await api.get('/admin/stats');
    return res.data;
  },

  getUsers: async (role) => {
    const res = await api.get('/admin/users', { params: { role } });
    return res.data;
  },

  toggleUserStatus: async (userId) => {
    const res = await api.patch(`/admin/users/${userId}/toggle-status`);
    return res.data;
  },

  deleteUser: async (userId) => {
    const res = await api.delete(`/admin/users/${userId}`);
    return res.data;
  },

  getDoctors: async () => {
    const res = await api.get('/admin/doctors');
    return res.data;
  },

  createDoctor: async (doctorData) => {
    const res = await api.post('/admin/doctors', doctorData);
    return res.data;
  },

  getNurses: async () => {
    const res = await api.get('/admin/nurses');
    return res.data;
  },

  createNurse: async (nurseData) => {
    const res = await api.post('/admin/nurses', nurseData);
    return res.data;
  },

  getDepartments: async () => {
    const res = await api.get('/admin/departments');
    return res.data;
  },

  createDepartment: async (deptData) => {
    const res = await api.post('/admin/departments', deptData);
    return res.data;
  },

  getAuditLogs: async () => {
    const res = await api.get('/admin/audit-logs');
    return res.data;
  }
};
