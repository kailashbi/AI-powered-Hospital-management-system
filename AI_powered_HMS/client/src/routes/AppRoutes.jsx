import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Auth Pages
import { Login } from '../pages/auth/Login';
import { Register } from '../pages/auth/Register';
import { ForgotPassword } from '../pages/auth/ForgotPassword';

// Layouts
import { AdminLayout } from '../layouts/AdminLayout';
import { DoctorLayout } from '../layouts/AdminLayout'; // Alias / Layouts
import { NurseLayout } from '../layouts/AdminLayout';
import { PatientLayout } from '../layouts/AdminLayout';

// Admin Pages
import { AdminDashboard } from '../pages/admin/Dashboard';
import { AdminUsers } from '../pages/admin/Users';
import { AdminDoctors } from '../pages/admin/Doctors';
import { AdminNurses } from '../pages/admin/Nurses';
import { AdminDepartments } from '../pages/admin/Departments';
import { AdminReports } from '../pages/admin/Reports';
import { AdminAuditLogs } from '../pages/admin/AuditLogs';
import { AdminSettings } from '../pages/admin/Settings';
import { AdminKafkaStream } from '../pages/admin/KafkaStream';

// Doctor Pages

import { DoctorDashboard } from '../pages/doctor/Dashboard';
import { DoctorPatients } from '../pages/doctor/Patients';
import { DoctorAppointments } from '../pages/doctor/Appointments';
import { DoctorMedicalRecords } from '../pages/doctor/MedicalRecords';
import { DoctorPredictions } from '../pages/doctor/Predictions';
import { DoctorPredictionHistory } from '../pages/doctor/PredictionHistory';

// Nurse Pages
import { NurseDashboard } from '../pages/nurse/Dashboard';
import { NursePatients } from '../pages/nurse/Patients';
import { NurseVitals } from '../pages/nurse/Vitals';
import { NurseDutyRoom } from '../pages/nurse/DutyRoom';

// Patient Pages
import { PatientDashboard } from '../pages/patient/Dashboard';
import { PatientProfile } from '../pages/patient/Profile';
import { PatientAppointments } from '../pages/patient/Appointments';
import { PatientMedicalRecords } from '../pages/patient/MedicalRecords';
import { PatientPredictions } from '../pages/patient/Predictions';

export const AppRoutes = () => {
  const { user, role } = useAuth();

  const getDefaultRedirect = () => {
    if (!user) return '/login';
    switch (role) {
      case 'admin': return '/admin';
      case 'doctor': return '/doctor';
      case 'nurse': return '/nurse';
      case 'patient': return '/patient';
      default: return '/doctor';
    }
  };

  return (
    <Routes>
      {/* Public Auth Routes */}
      <Route path="/login" element={!user ? <Login /> : <Navigate to={getDefaultRedirect()} replace />} />
      <Route path="/register" element={!user ? <Register /> : <Navigate to={getDefaultRedirect()} replace />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* Admin Protected Routes */}
      <Route path="/admin" element={<AdminLayout />}>
        <Route index element={<AdminDashboard />} />
        <Route path="users" element={<AdminUsers />} />
        <Route path="doctors" element={<AdminDoctors />} />
        <Route path="nurses" element={<AdminNurses />} />
        <Route path="departments" element={<AdminDepartments />} />
        <Route path="reports" element={<AdminReports />} />
        <Route path="audit-logs" element={<AdminAuditLogs />} />
        <Route path="kafka-stream" element={<AdminKafkaStream />} />
        <Route path="settings" element={<AdminSettings />} />

      </Route>

      {/* Doctor Protected Routes */}
      <Route path="/doctor" element={<DoctorLayout />}>
        <Route index element={<DoctorDashboard />} />
        <Route path="patients" element={<DoctorPatients />} />
        <Route path="appointments" element={<DoctorAppointments />} />
        <Route path="medical-records" element={<DoctorMedicalRecords />} />
        <Route path="predictions" element={<DoctorPredictions />} />
        <Route path="prediction-history" element={<DoctorPredictionHistory />} />
      </Route>

      {/* Nurse Protected Routes */}
      <Route path="/nurse" element={<NurseLayout />}>
        <Route index element={<NurseDashboard />} />
        <Route path="patients" element={<NursePatients />} />
        <Route path="vitals" element={<NurseVitals />} />
        <Route path="duty-room" element={<NurseDutyRoom />} />
      </Route>

      {/* Patient Protected Routes */}
      <Route path="/patient" element={<PatientLayout />}>
        <Route index element={<PatientDashboard />} />
        <Route path="profile" element={<PatientProfile />} />
        <Route path="appointments" element={<PatientAppointments />} />
        <Route path="medical-records" element={<PatientMedicalRecords />} />
        <Route path="predictions" element={<PatientPredictions />} />
      </Route>

      {/* Root Fallback */}
      <Route path="*" element={<Navigate to={getDefaultRedirect()} replace />} />
    </Routes>
  );
};
