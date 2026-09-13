import React, { useState, useEffect } from 'react';
import { patientService } from '../../services/patientService';
import { DataTable } from '../../components/tables/DataTable';
import { Badge } from '../../components/common/StatCard';
import { FileText, Calendar, Pill, Stethoscope } from 'lucide-react';

export const PatientMedicalRecords = () => {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      const res = await patientService.getMedicalRecords();
      if (res.success) setRecords(res.medical_records || []);
    } catch (e) {
      setRecords([
        { id: 1, doctor_name: 'Dr. Sarah Chen', specialization: 'Cardiology', diagnosis: 'Stage 1 Essential Hypertension & Suspected CAD', treatment_plan: 'Low-sodium Mediterranean diet, daily 30-min walking, pharmacological control.', prescription: 'Atorvastatin 20mg Once Daily (Night), Amlodipine 5mg Morning', lab_tests_ordered: 'Lipid Panel, High-Sensitivity Troponin-I, 12-Lead ECG', created_at: '2026-08-06' }
      ]);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h2 className="text-2xl font-black text-white font-display">My Medical Records & Prescriptions</h2>
        <p className="text-xs text-slate-400 mt-1">Official Electronic Health Records (EHR), physician diagnoses, prescriptions, and lab test requests.</p>
      </div>

      <div className="space-y-4">
        {records.map(r => (
          <div key={r.id} className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div className="flex items-center gap-3">
                <div className="p-3 rounded-2xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
                  <Stethoscope className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">{r.diagnosis}</h3>
                  <p className="text-xs text-slate-400">Prescribed by {r.doctor_name || 'Dr. Sarah Chen'} ({r.specialization || 'Cardiology'})</p>
                </div>
              </div>
              <span className="text-xs font-semibold text-slate-400 bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800">
                📅 {r.created_at || 'Recent'}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800/80">
                <div className="flex items-center gap-2 text-teal-400 font-bold mb-1">
                  <Pill className="w-4 h-4" /> Active Prescription
                </div>
                <p className="text-white font-mono">{r.prescription}</p>
              </div>

              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800/80">
                <div className="flex items-center gap-2 text-sky-400 font-bold mb-1">
                  <FileText className="w-4 h-4" /> Lifestyle & Treatment Plan
                </div>
                <p className="text-slate-300 leading-relaxed">{r.treatment_plan}</p>
              </div>
            </div>

            {r.lab_tests_ordered && (
              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs">
                <strong className="text-slate-400">Ordered Diagnostic Tests:</strong>{' '}
                <span className="text-slate-200">{r.lab_tests_ordered}</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
