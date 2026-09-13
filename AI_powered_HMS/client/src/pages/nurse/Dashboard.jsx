import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { nurseService } from '../../services/nurseService';
import { StatCard } from '../../components/common/StatCard';
import { Badge } from '../../components/common/StatCard';
import { 
  HeartPulse, 
  Activity, 
  BedDouble, 
  AlertTriangle, 
  Plus, 
  Users, 
  Clock,
  ShieldAlert
} from 'lucide-react';

export const NurseDashboard = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDash = async () => {
      try {
        const res = await nurseService.getDashboard();
        if (res.success) setData(res);
      } catch (err) {
        console.warn("Nurse dash fallback:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDash();
  }, []);

  const stats = data?.stats || {
    total_patients: 12,
    vitals_recorded_today: 8,
    abnormal_readings_flagged: 2,
    current_duty_status: 'On Duty',
    assigned_room: 'Cardiac Care Unit - CCU 301'
  };

  const recentVitals = data?.recent_vitals || [
    { id: 1, recorded_at: '2026-08-08 08:15', bp_display: '165/105 mmHg', heart_rate: 92, spo2: 96, temperature: 99.1, is_abnormal: true, notes: 'Hypertension flagged for Dr. Rostova' },
    { id: 2, recorded_at: '2026-08-08 07:45', bp_display: '138/88 mmHg', heart_rate: 78, spo2: 98, temperature: 98.4, is_abnormal: false, notes: 'Post-morning stabilizing vitals' }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Welcome Banner */}
      <div className="glass-card p-6 rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900 to-teal-950/40 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-teal-500/20 text-teal-300 border border-teal-500/30 uppercase">
              Triage & Nursing Care
            </span>
            <span className="text-xs text-slate-400">Nurse Emily Watson (CCU Specialist)</span>
          </div>
          <h2 className="text-2xl font-black text-white font-display">Vitals Telemetry & Ward Duty Hub</h2>
          <p className="text-xs text-slate-400 mt-1">Record physiological biomarkers, monitor critical alerts, and manage ward bed assignments.</p>
        </div>

        <button
          onClick={() => navigate('/nurse/vitals')}
          className="px-5 py-3 rounded-2xl bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-400 hover:to-emerald-400 text-white font-extrabold text-xs shadow-lg shadow-teal-500/30 flex items-center gap-2 transition-all hover:scale-105"
        >
          <Activity className="w-4 h-4" /> Record New Patient Vitals
        </button>
      </div>

      {/* Top Clinical Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Assigned Ward" value={stats.assigned_room} subtitle="Active Shift Area" icon={BedDouble} color="teal" />
        <StatCard title="Vitals Logged Today" value={stats.vitals_recorded_today} subtitle="Telemetry recordings" icon={Activity} color="sky" />
        <StatCard title="Abnormal Readings" value={stats.abnormal_readings_flagged} subtitle="Notified attending physician" icon={AlertTriangle} color="rose" />
        <StatCard title="Duty Status" value={stats.current_duty_status} subtitle="Morning Shift (06:00 - 14:00)" icon={Clock} color="emerald" />
      </div>

      {/* Recent Vitals Feed & Ward Roster */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-card rounded-3xl border border-slate-800 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold text-white">Recent Vital Sign Telemetry</h3>
            <button
              onClick={() => navigate('/nurse/vitals')}
              className="text-xs font-semibold text-teal-400 hover:text-teal-300"
            >
              Log New Vitals →
            </button>
          </div>

          <div className="space-y-3">
            {recentVitals.map(v => (
              <div key={v.id} className={`p-4 rounded-2xl border transition-all ${v.is_abnormal ? 'bg-rose-950/20 border-rose-500/40 animate-pulse' : 'bg-slate-900/60 border-slate-800/80'}`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-white text-sm">Blood Pressure: {v.bp_display}</span>
                    {v.is_abnormal && <Badge variant="critical">Abnormal Flag</Badge>}
                  </div>
                  <span className="text-[11px] text-slate-400">{v.recorded_at}</span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-xs text-slate-300">
                  <div>Heart Rate: <strong className="text-sky-400">{v.heart_rate} BPM</strong></div>
                  <div>SpO2: <strong className="text-emerald-400">{v.spo2}%</strong></div>
                  <div>Temp: <strong className="text-amber-400">{v.temperature}°F</strong></div>
                </div>

                {v.notes && <p className="text-[11px] text-slate-400 mt-2 italic">Note: {v.notes}</p>}
              </div>
            ))}
          </div>
        </div>

        {/* Duty & Room Quick Card */}
        <div className="glass-card rounded-3xl border border-slate-800 p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <BedDouble className="w-5 h-5 text-teal-400" />
              <h3 className="text-base font-bold text-white">Nurse Duty Roster</h3>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase font-bold">Assigned Ward / Bed Units</span>
                <span className="font-bold text-white text-sm">{stats.assigned_room}</span>
              </div>

              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase font-bold">Shift Schedule</span>
                <span className="font-bold text-teal-400">Morning (06:00 - 14:00)</span>
              </div>

              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase font-bold">Emergency Code Status</span>
                <span className="font-bold text-emerald-400">Ready for Code Blue Dispatch</span>
              </div>
            </div>
          </div>

          <button
            onClick={() => navigate('/nurse/duty-room')}
            className="w-full mt-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 font-bold text-xs text-teal-400 border border-slate-700"
          >
            Update Shift & Room Roster →
          </button>
        </div>
      </div>
    </div>
  );
};
