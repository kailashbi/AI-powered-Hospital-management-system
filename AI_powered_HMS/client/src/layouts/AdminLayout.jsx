import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { TopNavbar } from '../components/navbar/TopNavbar';
import { Sidebar } from '../components/sidebar/Sidebar';
import { LoadingSpinner } from '../components/common/StatCard';

const BaseLayout = ({ allowedRole }) => {
  const { user, role, loading } = useAuth();

  if (loading) return <LoadingSpinner label="Authenticating session..." />;

  // If not logged in, redirect to login
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <TopNavbar />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar />
        <main className="flex-1 p-4 lg:p-8 overflow-y-auto max-h-[calc(100vh-65px)]">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export const AdminLayout = () => <BaseLayout allowedRole="admin" />;
export const DoctorLayout = () => <BaseLayout allowedRole="doctor" />;
export const NurseLayout = () => <BaseLayout allowedRole="nurse" />;
export const PatientLayout = () => <BaseLayout allowedRole="patient" />;
