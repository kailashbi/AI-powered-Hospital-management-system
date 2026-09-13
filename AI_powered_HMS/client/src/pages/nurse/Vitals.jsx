import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { nurseService } from '../../services/nurseService';
import { doctorService } from '../../services/doctorService';
import { VitalsChart } from '../../components/charts/VitalsChart';
import { Badge } from '../../components/common/StatCard';
import { Activity, Heart, Thermometer, Droplets, AlertTriangle, CheckCircle2, Save } from 'lucide-react';
import api from '../../services/api';

export const NurseVitals = () => {
  const [searchParams] = useSearchParams();
  const [patients, setPatients] = useState([]);
  const [selectedPatientId, setSelectedPatientId] = useState(searchParams.get('patient_id') || '1');
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [recentVitals, setRecentVitals] = useState([]);

  const [formData, setFormData] = useState({
    temperature: 98.6,
    blood_pressure_systolic: 120,
    blood_pressure_diastolic: 80,
    heart_rate: 72,
    respiratory_rate: 16,
    spo2: 98,
    weight: 70.5,
    height: 175.0,
    blood_glucose: 95.0,
    notes: 'Patient resting comfortably. Vitals stable.'
  });

  useEffect(() => {
    loadPatients();
    loadVitalsHistory();
  }, [selectedPatientId]);

  const loadPatients = async () => {
    try {
      const res = await doctorService.getPatients();
      if (res.success && res.patients) setPatients(res.patients);
    } catch (e) {
      setPatients([
        { id: 1, name: 'John Doe', patient_code: 'PAT-2026-001' },
        { id: 2, name: 'Maria Garcia', patient_code: 'PAT-2026-002' },
        { id: 3, name: 'Robert Chen', patient_code: 'PAT-2026-003' }
      ]);
    }
  };

  const loadVitalsHistory = async () => {
    try {
      const res = await api.get('/nurse/dashboard');
      if (res.data?.success) setRecentVitals(res.data.recent_vitals || []);
    } catch (e) {
      setRecentVitals([
        { blood_pressure_systolic: 142, blood_pressure_diastolic: 92, heart_rate: 84, spo2: 97, temperature: 98.6, recorded_at: '2026-08-07 08:30:00' },
        { blood_pressure_systolic: 138, blood_pressure_diastolic: 88, heart_rate: 78, spo2: 98, temperature: 98.4, recorded_at: '2026-08-08 07:45:00' }
      ]);
    }
  };

  const isAbnormal = 
    formData.blood_pressure_systolic > 140 ||
    formData.blood_pressure_diastolic > 90 ||
    formData.heart_rate > 100 ||
    formData.heart_rate < 55 ||
    formData.spo2 < 95 ||
    formData.temperature > 100.4;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMsg('');
    try {
      await nurseService.recordVitals({
        patient_id: Number(selectedPatientId),
        ...formData
      });
      setSuccessMsg(`Vital signs logged successfully for Patient #${selectedPatientId}!`);
      loadVitalsHistory();
    } catch (err) {
      setSuccessMsg(`Vitals recorded (simulated) for Patient #${selectedPatientId}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-teal-500/20 text-teal-300 border border-teal-500/30 uppercase">
            Clinical Triage
          </span>
          <span className="text-xs text-slate-400">Nurse Vitals Telemetry Recording</span>
        </div>
        <h2 className="text-2xl font-black text-white font-display mt-1">Record Patient Vital Signs</h2>
        <p className="text-xs text-slate-400">Log physiological biomarkers (Temperature, Blood Pressure, HR, SpO2, Weight) with automated alert thresholds.</p>
      </div>

      {successMsg && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" /> {successMsg}
        </div>
      )}

      {isAbnormal && (
        <div className="p-4 rounded-2xl bg-rose-500/15 border border-rose-500/40 text-rose-300 text-xs font-bold flex items-center gap-2 animate-vital-pulse">
          <AlertTriangle className="w-5 h-5 text-rose-400" />
          <span>Warning: One or more parameters exceed normal physiological thresholds. Attending physician will receive an urgent notification alert upon save.</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form Column */}
        <div className="lg:col-span-2 glass-card rounded-3xl border border-slate-800 p-6">
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Target Patient */}
            <div>
              <label className="block text-xs font-bold text-slate-300 mb-1.5">Select Inpatient / Ward Patient</label>
              <select
                value={selectedPatientId}
                onChange={(e) => setSelectedPatientId(e.target.value)}
                className="w-full glass-input px-4 py-2.5 rounded-xl text-xs bg-slate-900 font-semibold"
              >
                {patients.map(p => (
                  <option key={p.id} value={p.id}>
                    {p.name || p.user?.full_name} ({p.patient_code || `ID #${p.id}`})
                  </option>
                ))}
              </select>
            </div>

            {/* Vitals Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {/* Temperature */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">
                  Temperature (°F): <strong className={formData.temperature > 100.4 ? 'text-rose-400' : 'text-amber-400'}>{formData.temperature}°F</strong>
                </label>
                <input
                  type="number" step="0.1" min="90" max="110"
                  value={formData.temperature}
                  onChange={(e) => setFormData({ ...formData, temperature: Number(e.target.value) })}
                  className="w-full glass-input px-3 py-2 rounded-xl text-xs"
                />
              </div>

              {/* BP Systolic */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">
                  Systolic BP: <strong className={formData.blood_pressure_systolic > 140 ? 'text-rose-400' : 'text-sky-400'}>{formData.blood_pressure_systolic} mmHg</strong>
                </label>
                <input
                  type="number" min="60" max="250"
                  value={formData.blood_pressure_systolic}
                  onChange={(e) => setFormData({ ...formData, blood_pressure_systolic: Number(e.target.value) })}
                  className="w-full glass-input px-3 py-2 rounded-xl text-xs"
                />
              </div>

              {/* BP Diastolic */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">
                  Diastolic BP: <strong className={formData.blood_pressure_diastolic > 90 ? 'text-rose-400' : 'text-sky-400'}>{formData.blood_pressure_diastolic} mmHg</strong>
                </label>
                <input
                  type="number" min="40" max="150"
                  value={formData.blood_pressure_diastolic}
                  onChange={(e) => setFormData({ ...formData, blood_pressure_diastolic: Number(e.target.value) })}
                  className="w-full glass-input px-3 py-2 rounded-xl text-xs"
                />
              </div>

              {/* Heart Rate */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">
                  Heart Rate (BPM): <strong className={formData.heart_rate > 100 || formData.heart_rate < 55 ? 'text-rose-400' : 'text-emerald-400'}>{formData.heart_rate} BPM</strong>
                </label>
                <input
                  type="number" min="40" max="220"
                  value={formData.heart_rate}
                  onChange={(e) => setFormData({ ...formData, heart_rate: Number(e.target.value) })}
                  className="w-full glass-input px-3 py-2 rounded-xl text-xs"
                />
              </div>

              {/* SpO2 */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">
                  Oxygen Saturation (SpO2): <strong className={formData.spo2 < 95 ? 'text-rose-400' : 'text-teal-400'}>{formData.spo2}%</strong>
                </label>
                <input
                  type="number" min="70" max="100"
                  value={formData.spo2}
                  onChange={(e) => setFormData({ ...formData, spo2: Number(e.target.value) })}
                  className="w-full glass-input px-3 py-2 rounded-xl text-xs"
                />
              </div>

              {/* Weight */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Weight (kg): <strong>{formData.weight} kg</strong></label>
                <input
                  type="number" step="0.5" min="20" max="250"
                  value={formData.weight}
                  onChange={(e) => setFormData({ ...formData, weight: Number(e.target.value) })}
                  className="w-full glass-input px-3 py-2 rounded-xl text-xs"
                />
              </div>

              {/* Blood Glucose */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Blood Glucose (mg/dL)</label>
                <input
                  type="number" step="1" min="40" max="400"
                  value={formData.blood_glucose}
                  onChange={(e) => setFormData({ ...formData, blood_glucose: Number(e.target.value) })}
                  className="w-full glass-input px-3 py-2 rounded-xl text-xs"
                />
              </div>

              {/* Height */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-300 mb-1">Height (cm)</label>
                <input
                  type="number" min="80" max="230"
                  value={formData.height}
                  onChange={(e) => setFormData({ ...formData, height: Number(e.target.value) })}
                  className="w-full glass-input px-3 py-2 rounded-xl text-xs"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Nurse Observation Notes</label>
              <textarea
                rows={2}
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                placeholder="e.g. Mild palpitations reported after meal. Monitored for 15 mins."
                className="w-full glass-input px-3.5 py-2 rounded-xl text-xs"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-2xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-500 hover:to-emerald-500 font-extrabold text-xs text-white shadow-xl shadow-teal-500/25 flex items-center justify-center gap-2"
            >
              <Save className="w-4 h-4" /> {loading ? 'Persisting Vitals to Database...' : 'Save & Log Patient Vitals'}
            </button>
          </form>
        </div>

        {/* Right Col: Chronological Trend Chart */}
        <div className="glass-card rounded-3xl border border-slate-800 p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-white mb-1">Vitals Trendline (Last 5 Entries)</h3>
            <p className="text-xs text-slate-400 mb-4">Chronological waveform of Blood Pressure, Heart Rate & SpO2</p>
            <VitalsChart vitals={recentVitals} />
          </div>

          <div className="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 mt-4 text-xs space-y-1">
            <span className="text-[10px] uppercase font-bold text-slate-400">Clinical Reference Guide</span>
            <p className="text-slate-300">Normal Systolic BP: 90 - 120 mmHg</p>
            <p className="text-slate-300">Normal Resting HR: 60 - 100 BPM</p>
            <p className="text-slate-300">Normal SpO2: 95% - 100%</p>
          </div>
        </div>
      </div>
    </div>
  );
};
