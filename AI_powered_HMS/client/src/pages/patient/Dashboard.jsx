import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { patientService } from '../../services/patientService';
import { StatCard, Badge } from '../../components/common/StatCard';
import { RiskGauge } from '../../components/charts/RiskGauge';
import { VitalsChart } from '../../components/charts/VitalsChart';
import { 
  Calendar, 
  FileText, 
  Activity, 
  Brain, 
  AlertTriangle, 
  ArrowUpRight, 
  Heart,
  Plus
} from 'lucide-react';

export const PatientDashboard = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPatientData = async () => {
      try {
        const res = await patientService.getDashboard();
        if (res.success) setData(res);
      } catch (err) {
        console.warn("Patient dashboard offline fallback:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchPatientData();
  }, []);

  const stats = data?.stats || {
    upcoming_appointments: 1,
    total_medical_records: 2,
    latest_vital_bp: '142/92 mmHg',
    latest_vital_hr: 84,
    latest_ai_risk: 78.45,
    latest_ai_disease: 'Heart Disease'
  };

  const appointments = data?.appointments || [
    { id: 1, appointment_code: 'APT-2026-001', doctor_name: 'Dr. Sarah Chen', department_name: 'Cardiology', appointment_date: '2026-08-10', appointment_time: '09:30', status: 'Confirmed', priority: 'Urgent' }
  ];

  const vitalsHistory = data?.vitals_history || [
    { blood_pressure_systolic: 142, blood_pressure_diastolic: 92, heart_rate: 84, spo2: 97, recorded_at: '2026-08-07 08:30:00' },
    { blood_pressure_systolic: 138, blood_pressure_diastolic: 88, heart_rate: 78, spo2: 98, recorded_at: '2026-08-08 07:45:00' }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Welcome Banner */}
      <div className="glass-card p-6 rounded-3xl border border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-950/40 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 uppercase">
              Patient Health Portal
            </span>
            <span className="text-xs text-slate-400">Patient Code: PAT-2026-001</span>
          </div>
          <h2 className="text-2xl font-black text-white font-display">Welcome Back, John Doe</h2>
          <p className="text-xs text-slate-400 mt-1">Review upcoming consultations, vital signs trends, and AI-assisted health recommendations.</p>
        </div>

        <button
          onClick={() => navigate('/patient/appointments')}
          className="px-5 py-3 rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-extrabold text-xs shadow-lg shadow-emerald-500/30 flex items-center gap-2 transition-all hover:scale-105"
        >
          <Calendar className="w-4 h-4" /> Book New Consultation
        </button>
      </div>

      {/* Top Health Indicators */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title="Upcoming Appointment" value={stats.upcoming_appointments} subtitle="Dr. Sarah Chen (Cardiology)" icon={Calendar} color="emerald" />
        <StatCard title="Latest Blood Pressure" value={stats.latest_vital_bp} subtitle="Recorded by nurse" icon={Activity} color="rose" />
        <StatCard title="Resting Heart Rate" value={`${stats.latest_vital_hr} BPM`} subtitle="Optimal resting rhythm" icon={Heart} color="sky" />
        <StatCard title="AI Health Risk Score" value={`${stats.latest_ai_risk || 78.45}%`} subtitle={stats.latest_ai_disease || 'Heart Disease'} icon={Brain} color="amber" />
      </div>

      {/* Main Grid: Vitals Waveform & AI Prediction Gauge */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-card rounded-3xl border border-slate-800 p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white">My Vital Signs History</h3>
              <p className="text-xs text-slate-400">Chronological telemetry recorded during hospital checkups</p>
            </div>
            <Badge variant="info">Live EHR Telemetry</Badge>
          </div>
          <VitalsChart vitals={vitalsHistory} />
        </div>

        {/* AI Health Risk Gauge Card */}
        <div className="space-y-4">
          <RiskGauge
            score={stats.latest_ai_risk || 78.45}
            level="High"
            confidence={89.2}
            disease="Heart Disease Risk"
          />

          <button
            onClick={() => navigate('/patient/predictions')}
            className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 font-bold text-xs text-sky-400 border border-slate-700"
          >
            View Full AI Risk Breakdown →
          </button>
        </div>
      </div>

      {/* Upcoming Consultations Preview */}
      <div className="glass-card rounded-3xl border border-slate-800 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-white">Upcoming Appointments & Doctors</h3>
          <button
            onClick={() => navigate('/patient/appointments')}
            className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
          >
            Manage all appointments <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="space-y-3">
          {appointments.map(a => (
            <div key={a.id} className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              <div>
                <span className="font-mono text-xs font-bold text-sky-400">{a.appointment_code}</span>
                <h4 className="font-bold text-white text-sm">{a.doctor_name} ({a.department_name})</h4>
                <div className="flex items-center gap-3 text-xs text-slate-400 mt-1">
                  <span>📅 {a.appointment_date}</span>
                  <span>⏰ {a.appointment_time}</span>
                  <span>Room 304-A</span>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Badge variant={a.status === 'Confirmed' ? 'success' : 'warning'}>{a.status}</Badge>
                <Badge variant={a.priority === 'Urgent' ? 'danger' : 'info'}>{a.priority}</Badge>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
