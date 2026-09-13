import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminService } from '../../services/adminService';
import { StatCard, Badge } from '../../components/common/StatCard';
import { DepartmentChart } from '../../components/charts/DepartmentChart';
import { 
  Users, 
  Stethoscope, 
  HeartPulse, 
  Building2, 
  Calendar, 
  Activity, 
  ShieldCheck, 
  ArrowUpRight,
  ClipboardList
} from 'lucide-react';

export const AdminDashboard = () => {
  const navigate = useNavigate();
  const [statsData, setStatsData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await adminService.getStats();
      if (res.success) setStatsData(res);
    } catch (err) {
      console.warn("Admin stats offline fallback:", err);
    } finally {
      setLoading(false);
    }
  };

  const stats = statsData?.stats || {
    total_users: 10,
    active_doctors: 3,
    active_nurses: 2,
    total_patients: 4,
    total_appointments: 4,
    total_predictions: 3,
    high_risk_predictions: 2,
    bed_occupancy_rate: 78.5
  };

  const departments = statsData?.department_distribution || [
    { name: 'Cardiology', doctors: 1, nurses: 1, appointments: 2 },
    { name: 'Endocrinology', doctors: 1, nurses: 0, appointments: 2 },
    { name: 'Neurology', doctors: 1, nurses: 0, appointments: 1 },
    { name: 'Internal Med', doctors: 0, nurses: 1, appointments: 1 }
  ];

  const recentLogs = statsData?.recent_logs || [
    { action: 'RUN_AI_PREDICTION', entity_type: 'Prediction', user_name: 'Dr. Sarah Chen', created_at: '2026-08-08 09:12' },
    { action: 'RECORD_VITALS', entity_type: 'Vital', user_name: 'Nurse Emily Watson', created_at: '2026-08-08 08:30' },
    { action: 'CREATE_DOCTOR', entity_type: 'Doctor', user_name: 'Admin Vance', created_at: '2026-08-07 16:00' }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Admin Banner */}
      <div className="glass-card p-6 rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900 to-rose-950/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-rose-500/20 text-rose-300 border border-rose-500/30 uppercase">
              Hospital HQ & Governance
            </span>
            <span className="text-xs text-slate-400">Chief Medical Administrator (Dr. Arthur Vance)</span>
          </div>
          <h2 className="text-2xl font-black text-white font-display">Hospital Operations & Intelligence HQ</h2>
          <p className="text-xs text-slate-400 mt-1">Real-time facility capacity, medical staff allocation, and clinical AI governance telemetry.</p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => navigate('/admin/doctors')}
            className="px-4 py-2.5 rounded-2xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700"
          >
            Manage Staff Roster
          </button>
          <button
            onClick={() => navigate('/admin/reports')}
            className="px-4 py-2.5 rounded-2xl bg-gradient-to-r from-rose-600 to-sky-600 font-bold text-xs text-white shadow-lg"
          >
            Analytics Reports
          </button>
        </div>
      </div>

      {/* Top 4 KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Active Physicians" value={stats.active_doctors} subtitle="Certified specialists" icon={Stethoscope} color="sky" />
        <StatCard title="Nursing Staff" value={stats.active_nurses} subtitle="Active ward triage" icon={HeartPulse} color="teal" />
        <StatCard title="Bed Occupancy" value={`${stats.bed_occupancy_rate}%`} subtitle="Optimal clinical capacity" icon={Building2} color="amber" />
        <StatCard title="AI Diagnostic Volume" value={stats.total_predictions} subtitle={`${stats.high_risk_predictions} flagged critical`} icon={Activity} color="rose" />
      </div>

      {/* Main Grid: Department Workload & Real-time Audit Trace */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-card rounded-3xl border border-slate-800 p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white">Department Staff Allocation & Patient Volume</h3>
              <p className="text-xs text-slate-400">Real-time distribution across clinical departments</p>
            </div>
            <button
              onClick={() => navigate('/admin/departments')}
              className="text-xs font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1"
            >
              Manage Departments <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <DepartmentChart departments={departments} />
        </div>

        {/* Recent Audit Logs */}
        <div className="glass-card rounded-3xl border border-slate-800 p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <ClipboardList className="w-5 h-5 text-rose-400" />
                <h3 className="text-base font-bold text-white">Live Audit Logs</h3>
              </div>
              <Badge variant="default">HIPAA Log</Badge>
            </div>

            <div className="space-y-3">
              {recentLogs.map((log, i) => (
                <div key={i} className="p-3 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sky-300 font-mono text-[11px]">{log.action}</span>
                    <span className="text-[10px] text-slate-500">{log.created_at?.split('T')[0] || 'Recent'}</span>
                  </div>
                  <p className="text-slate-300">{log.user_name || 'Medical Staff'} on {log.entity_type}</p>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => navigate('/admin/audit-logs')}
            className="w-full mt-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 font-bold text-xs text-slate-300 border border-slate-700"
          >
            View Complete Audit Trail →
          </button>
        </div>
      </div>
    </div>
  );
};
