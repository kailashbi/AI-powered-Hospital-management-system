import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { doctorService } from '../../services/doctorService';
import { StatCard } from '../../components/common/StatCard';
import { Badge } from '../../components/common/StatCard';
import { 
  Users, 
  Calendar, 
  Brain, 
  AlertTriangle, 
  ArrowUpRight, 
  Stethoscope,
  Activity,
  Plus
} from 'lucide-react';

export const DoctorDashboard = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDash = async () => {
      try {
        const res = await doctorService.getDashboard();
        if (res.success) setData(res);
      } catch (err) {
        console.warn("Doctor dash offline fallback:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDash();
  }, []);

  const stats = data?.stats || {
    total_patients: 12,
    upcoming_appointments: 4,
    total_predictions_run: 18,
    critical_cases: 2
  };

  const appointments = data?.appointments || [
    { id: 1, appointment_code: 'APT-2026-001', patient_name: 'John Doe', appointment_date: '2026-08-10', appointment_time: '09:30', priority: 'Urgent', status: 'Confirmed', symptoms: 'Intermittent chest tightness, shortness of breath' },
    { id: 2, appointment_code: 'APT-2026-002', patient_name: 'Maria Garcia', appointment_date: '2026-08-11', appointment_time: '11:00', priority: 'Urgent', status: 'Scheduled', symptoms: 'Episodic dizziness and elevated blood pressure' }
  ];

  const criticalAlerts = data?.critical_alerts || [
    { id: 1, patient_name: 'Maria Garcia', disease_type: 'Stroke', risk_score: 84.10, risk_level: 'Critical', clinical_recommendation: 'Urgent carotid doppler and blood pressure stabilization required.' },
    { id: 2, patient_name: 'John Doe', disease_type: 'Heart Disease', risk_score: 78.45, risk_level: 'High', clinical_recommendation: 'Stress echocardiogram and statin intensification advised.' }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Welcome Banner & Quick Action */}
      <div className="glass-card p-6 rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900 to-sky-950/40 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-sky-500/20 text-sky-300 border border-sky-500/30 uppercase">
              Clinical Workspace
            </span>
            <span className="text-xs text-slate-400">Dr. Sarah Chen (Cardiology)</span>
          </div>
          <h2 className="text-2xl font-black text-white font-display">Physician Diagnostics & AI Decision Support</h2>
          <p className="text-xs text-slate-400 mt-1">Review active patient queues, vitals telemetry, and run automated disease risk evaluations.</p>
        </div>

        <button
          onClick={() => navigate('/doctor/predictions')}
          className="px-5 py-3 rounded-2xl bg-gradient-to-r from-sky-500 to-teal-500 hover:from-sky-400 hover:to-teal-400 text-white font-extrabold text-xs shadow-lg shadow-sky-500/30 flex items-center gap-2 transition-all hover:scale-105"
        >
          <Brain className="w-4 h-4" /> Run AI Diagnostic Assessment
        </button>
      </div>

      {/* Top Clinical Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Assigned Patients" value={stats.total_patients} subtitle="Active under your care" icon={Users} color="sky" />
        <StatCard title="Upcoming Consultations" value={stats.upcoming_appointments} subtitle="Scheduled this week" icon={Calendar} color="indigo" />
        <StatCard title="AI Predictions Run" value={stats.total_predictions_run} subtitle="Heart, Diabetes, Stroke" icon={Brain} color="teal" />
        <StatCard title="Critical Risk Alerts" value={stats.critical_cases} subtitle="Requiring priority attention" icon={AlertTriangle} color="rose" />
      </div>

      {/* Main Grid: Priority Consultations & Critical AI Warnings */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upcoming Consultations */}
        <div className="lg:col-span-2 glass-card rounded-3xl border border-slate-800 p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white">Upcoming Patient Consultations</h3>
              <p className="text-xs text-slate-400">Upcoming clinical reviews and schedule</p>
            </div>
            <button
              onClick={() => navigate('/doctor/appointments')}
              className="text-xs font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1"
            >
              View all <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-3">
            {appointments.map(a => (
              <div key={a.id} className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 hover:border-slate-700 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20 flex items-center justify-center font-bold text-sm">
                    {a.patient_name ? a.patient_name[0] : 'P'}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white">{a.patient_name}</h4>
                    <p className="text-xs text-slate-400">{a.symptoms || 'General medical follow up'}</p>
                    <div className="flex items-center gap-2 mt-1 text-[11px] text-slate-400">
                      <span>📅 {a.appointment_date}</span>
                      <span>⏰ {a.appointment_time}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-end sm:self-center">
                  <Badge variant={a.priority === 'Urgent' ? 'danger' : 'info'}>{a.priority}</Badge>
                  <button
                    onClick={() => navigate(`/doctor/patients`)}
                    className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200"
                  >
                    Examine EHR
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Critical AI Alerts */}
        <div className="glass-card rounded-3xl border border-slate-800 p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
                  <AlertTriangle className="w-4 h-4 animate-pulse" />
                </div>
                <h3 className="text-base font-bold text-white">Critical Risk Alerts</h3>
              </div>
              <Badge variant="critical">Urgent</Badge>
            </div>

            <div className="space-y-3">
              {criticalAlerts.map(alert => (
                <div key={alert.id} className="p-3.5 rounded-2xl bg-rose-950/20 border border-rose-500/30 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-xs text-white">{alert.patient_name}</span>
                    <span className="text-xs font-extrabold text-rose-400">{alert.disease_type} ({alert.risk_score}%)</span>
                  </div>
                  <p className="text-[11px] text-slate-300 leading-relaxed">{alert.clinical_recommendation}</p>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => navigate('/doctor/predictions')}
            className="w-full mt-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-sky-400 border border-slate-700"
          >
            Launch Prediction Lab →
          </button>
        </div>
      </div>
    </div>
  );
};
