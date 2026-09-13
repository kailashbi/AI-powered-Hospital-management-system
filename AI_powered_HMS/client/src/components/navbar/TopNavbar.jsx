import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { 
  Bell, 
  ShieldCheck, 
  Stethoscope, 
  HeartPulse, 
  User, 
  LogOut, 
  ChevronDown, 
  CheckCheck,
  AlertTriangle,
  Calendar
} from 'lucide-react';
import api from '../../services/api';

export const TopNavbar = () => {
  const navigate = useNavigate();
  const { user, role, quickSwitch, logout } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [showNotifMenu, setShowNotifMenu] = useState(false);
  const [showRoleMenu, setShowRoleMenu] = useState(false);

  useEffect(() => {
    const fetchNotifs = async () => {
      try {
        const res = await api.get('/notifications');
        if (res.data?.success) {
          setNotifications(res.data.notifications || []);
        }
      } catch (err) {
        // Fallback targeted notifications for demo user context
        if (user?.role === 'patient') {
          setNotifications([
            { id: 101, user_id: user?.id, title: `Personalized AI Health Update for ${user?.first_name || 'Patient'}`, message: 'Dr. Ankit reviewed your cardiovascular diagnostic report and updated your prescription plan.', type: 'AI Alert', is_read: false, created_at: 'Just now' },
            { id: 102, user_id: user?.id, title: 'Cardiology Appointment Confirmed', message: 'Your follow-up consult with Dr. Ankit is scheduled for tomorrow at 10:00 AM.', type: 'Appointment', is_read: false, created_at: '25m ago' }
          ]);
        } else if (user?.role === 'doctor') {
          setNotifications([
            { id: 201, user_id: user?.id, title: 'New Critical Vitals Recorded', message: 'Nurse Sunder submitted elevated BP (165/105 mmHg) for Mukesh.', type: 'Vital Warning', is_read: false, created_at: '10m ago' }
          ]);
        } else if (user?.role === 'nurse') {
          setNotifications([
            { id: 301, user_id: user?.id, title: 'Shift Duty Assignment', message: 'Assigned to Cardiac Care Unit (CCU 301) for morning triage.', type: 'General', is_read: false, created_at: '1h ago' }
          ]);
        } else {
          setNotifications([
            { id: 401, user_id: user?.id, title: 'System Security Audit', message: 'All hospital services operational; Kafka event telemetry active.', type: 'General', is_read: true, created_at: '2h ago' }
          ]);
        }
      }
    };
    if (user) fetchNotifs();
  }, [user]);

  const unreadCount = notifications.filter(n => !n.is_read).length;

  const markAllRead = async () => {
    try {
      await api.post('/notifications/mark-all-read');
    } catch (e) {
      console.warn("Offline notif read toggle");
    }
    setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
  };

  const getRoleIcon = (r) => {
    switch (r) {
      case 'admin': return <ShieldCheck className="w-4 h-4 text-rose-400" />;
      case 'doctor': return <Stethoscope className="w-4 h-4 text-sky-400" />;
      case 'nurse': return <HeartPulse className="w-4 h-4 text-teal-400" />;
      case 'patient': return <User className="w-4 h-4 text-emerald-400" />;
      default: return <User className="w-4 h-4 text-slate-400" />;
    }
  };

  const getRoleColor = (r) => {
    switch (r) {
      case 'admin': return 'bg-rose-500/10 text-rose-300 border-rose-500/30';
      case 'doctor': return 'bg-sky-500/10 text-sky-300 border-sky-500/30';
      case 'nurse': return 'bg-teal-500/10 text-teal-300 border-teal-500/30';
      case 'patient': return 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30';
      default: return 'bg-slate-700/50 text-slate-300 border-slate-600';
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-slate-900/80 backdrop-blur-xl border-b border-slate-800/80 px-4 lg:px-8 py-3 flex items-center justify-between shadow-sm">
      {/* Brand Logo & Medical Indicator */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-teal-500 flex items-center justify-center shadow-lg shadow-sky-500/20 text-white font-black text-xl tracking-wider">
          K+
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-extrabold text-lg lg:text-xl text-white tracking-tight font-display">
              KAIre <span className="text-sky-400 font-medium">Health</span>
            </h1>
            <span className="hidden sm:inline-block px-2 py-0.5 text-[10px] font-bold rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/30 uppercase tracking-wider">
              AI-HMS Enterprise
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-medium hidden md:block">Clinical Diagnostics & Role-Based EHR Intelligence</p>
        </div>
      </div>

      {/* Right Action Bar: Notification Dropdown & Profile Menu */}
      <div className="flex items-center gap-2 sm:gap-4">

        {/* Notifications Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowNotifMenu(!showNotifMenu)}
            className="relative p-2 rounded-xl bg-slate-800/80 border border-slate-700/80 hover:bg-slate-700/80 text-slate-300 hover:text-white transition-colors"
            title="Notifications & Clinical Alerts"
          >
            <Bell className="w-4 h-4" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-[10px] font-extrabold text-white flex items-center justify-center animate-bounce">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifMenu && (
            <div className="absolute right-0 mt-2 w-80 sm:w-96 glass-card rounded-2xl p-4 border border-slate-700/90 shadow-2xl z-50 animate-scaleUp">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <h4 className="text-sm font-bold text-white">Notifications</h4>
                  {unreadCount > 0 && (
                    <span className="px-1.5 py-0.5 text-[10px] rounded-full bg-rose-500/20 text-rose-300 font-bold">
                      {unreadCount} new
                    </span>
                  )}
                </div>
                {unreadCount > 0 && (
                  <button 
                    onClick={markAllRead}
                    className="text-xs text-sky-400 hover:text-sky-300 flex items-center gap-1 font-medium"
                  >
                    <CheckCheck className="w-3.5 h-3.5" /> Mark all read
                  </button>
                )}
              </div>

              <div className="mt-3 space-y-2.5 max-h-72 overflow-y-auto pr-1">
                {notifications.length === 0 ? (
                  <p className="text-xs text-slate-400 py-6 text-center">No alerts at this moment</p>
                ) : (
                  notifications.map(n => (
                    <div 
                      key={n.id} 
                      className={`p-3 rounded-xl border text-xs transition-all ${n.is_read ? 'bg-slate-900/40 border-slate-800/60 text-slate-400' : 'bg-sky-950/30 border-sky-800/50 text-slate-200 font-medium'}`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-bold text-white flex items-center gap-1.5">
                          {n.type === 'AI Alert' ? <AlertTriangle className="w-3.5 h-3.5 text-amber-400" /> : <Calendar className="w-3.5 h-3.5 text-sky-400" />}
                          {n.title}
                        </span>
                        <span className="text-[10px] text-slate-400">{n.created_at || 'Today'}</span>
                      </div>
                      <p className="text-slate-300 text-[11px] leading-relaxed">{n.message}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* User Badge & Logout */}
        <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
          <div className="hidden md:flex flex-col text-right">
            <span className="text-xs font-bold text-white leading-tight">{user?.full_name || 'Medical Staff'}</span>
            <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded-full border self-end mt-0.5 capitalize ${getRoleColor(role)}`}>
              {role}
            </span>
          </div>

          <img 
            src={user?.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'} 
            alt="Avatar"
            className="w-9 h-9 rounded-xl object-cover border border-slate-700 shadow-md"
          />

          <button
            onClick={logout}
            className="p-2 rounded-xl text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors ml-1"
            title="Sign out of KAIre Health"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
