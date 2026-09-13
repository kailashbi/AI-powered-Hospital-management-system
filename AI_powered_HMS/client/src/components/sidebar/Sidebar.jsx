import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  LayoutDashboard,
  Users,
  Stethoscope,
  HeartPulse,
  Building2,
  Calendar,
  FileText,
  Activity,
  Brain,
  History,
  ShieldCheck,
  ClipboardList,
  UserCheck,
  Settings,
  Radio,
  Sparkles,
  BedDouble
} from 'lucide-react';

export const Sidebar = () => {
  const { role, user } = useAuth();

  const getNavLinks = () => {
    switch (role) {
      case 'admin':
        return [
          { to: '/admin', label: 'Dashboard', icon: LayoutDashboard, exact: true },
          { to: '/admin/users', label: 'Users & Roles', icon: Users },
          { to: '/admin/doctors', label: 'Doctors Roster', icon: Stethoscope },
          { to: '/admin/nurses', label: 'Nursing Staff', icon: HeartPulse },
          { to: '/admin/departments', label: 'Departments', icon: Building2 },
          { to: '/admin/kafka-stream', label: 'Kafka Event Stream', icon: Radio, badge: 'Telemetry' },
          { to: '/admin/reports', label: 'Analytics Reports', icon: FileText },
          { to: '/admin/audit-logs', label: 'Audit Logs', icon: ClipboardList },
          { to: '/admin/settings', label: 'System Settings', icon: Settings },
        ];

      case 'doctor':
        return [
          { to: '/doctor', label: 'Dashboard', icon: LayoutDashboard, exact: true },
          { to: '/doctor/patients', label: 'My Patients', icon: Users },
          { to: '/doctor/appointments', label: 'Appointments', icon: Calendar },
          { to: '/doctor/medical-records', label: 'EHR Records', icon: FileText },
          { to: '/doctor/predictions', label: 'Run AI Prediction', icon: Brain, badge: 'ML AI' },
          { to: '/doctor/prediction-history', label: 'Prediction History', icon: History },
        ];
      case 'nurse':
        return [
          { to: '/nurse', label: 'Dashboard', icon: LayoutDashboard, exact: true },
          { to: '/nurse/patients', label: 'Patient Directory', icon: Users },
          { to: '/nurse/vitals', label: 'Record Vitals', icon: Activity, badge: 'Triage' },
          { to: '/nurse/duty-room', label: 'Duty & Rooms', icon: BedDouble },
        ];
      case 'patient':
        return [
          { to: '/patient', label: 'Dashboard', icon: LayoutDashboard, exact: true },
          { to: '/patient/profile', label: 'Patient Profile', icon: UserCheck },
          { to: '/patient/appointments', label: 'Appointments', icon: Calendar },
          { to: '/patient/medical-records', label: 'Medical Records', icon: FileText },
          { to: '/patient/predictions', label: 'AI Health Results', icon: Brain, badge: 'AI Insights' },
        ];
      default:
        return [];
    }
  };

  const navLinks = getNavLinks();

  return (
    <aside className="w-64 bg-slate-900/90 backdrop-blur-2xl border-r border-slate-800/80 min-h-[calc(100vh-65px)] p-4 flex flex-col justify-between hidden md:flex">
      <div className="space-y-6">
        {/* Role Portal Card */}
        <div className="p-3.5 rounded-2xl bg-gradient-to-br from-slate-800/80 to-slate-950 border border-slate-700/60 shadow-md">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <p className="text-[10px] uppercase font-extrabold text-sky-400 tracking-wider">Active Workspace</p>
              <h3 className="text-xs font-bold text-white capitalize">{role} Portal</h3>
            </div>
          </div>
        </div>

        {/* Navigation Section */}
        <nav className="space-y-1">
          <p className="px-3 text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-2">Navigation Menu</p>
          {navLinks.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.exact}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 group ${
                    isActive
                      ? 'bg-gradient-to-r from-sky-600 to-sky-500 text-white shadow-lg shadow-sky-500/20 font-bold'
                      : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-4 h-4 transition-transform group-hover:scale-110" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="px-1.5 py-0.5 text-[9px] font-extrabold rounded-md bg-sky-400/20 text-sky-200 border border-sky-300/30">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Model & Version Indicator footer */}
      <div className="pt-4 border-t border-slate-800/80">
        <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 text-[11px] text-slate-400">
          <div className="flex items-center justify-between mb-1">
            <span className="font-semibold text-slate-300">ML Engine</span>
            <span className="text-emerald-400 font-bold text-[10px]">● Online</span>
          </div>
          <p className="text-[10px] text-slate-400">Scikit-Learn + XGBoost (Heart, Diabetes, Stroke)</p>
        </div>
      </div>
    </aside>
  );
};
