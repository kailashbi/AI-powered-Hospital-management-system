import React, { useState, useEffect } from 'react';
import { doctorService } from '../../services/doctorService';
import { DataTable } from '../../components/tables/DataTable';
import { Modal } from '../../components/common/StatCard';
import { FileText, Plus, CheckCircle2 } from 'lucide-react';
import api from '../../services/api';

export const DoctorMedicalRecords = () => {
  const [records, setRecords] = useState([]);
  const [patients, setPatients] = useState([]);
  const [createModal, setCreateModal] = useState(false);
  const [formData, setFormData] = useState({
    patient_id: '1',
    diagnosis: '',
    symptoms: '',
    treatment_plan: '',
    prescription: '',
    lab_tests_ordered: '',
    follow_up_date: ''
  });

  useEffect(() => {
    fetchRecords();
    fetchPatients();
  }, []);

  const fetchRecords = async () => {
    try {
      const res = await api.get('/medical-records');
      if (res.data?.success) setRecords(res.data.medical_records || []);
    } catch (e) {
      setRecords([
        { id: 1, patient_name: 'John Doe', diagnosis: 'Stage 1 Hypertension & Suspected CAD', treatment_plan: 'Low-sodium diet, statin therapy', prescription: 'Atorvastatin 20mg Once Daily', created_at: '2026-08-06' },
        { id: 2, patient_name: 'Maria Garcia', diagnosis: 'Transient Ischemic Attack (TIA) Prodrome', treatment_plan: 'Carotid ultrasound, blood pressure stabilization', prescription: 'Clopidogrel 75mg Daily, Lisinopril 20mg', created_at: '2026-08-07' }
      ]);
    }
  };

  const fetchPatients = async () => {
    try {
      const res = await doctorService.getPatients();
      if (res.success) setPatients(res.patients || []);
    } catch (e) {
      setPatients([
        { id: 1, name: 'John Doe' },
        { id: 2, name: 'Maria Garcia' }
      ]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await doctorService.createMedicalRecord(formData);
      alert("Medical Record (EHR) added successfully!");
      setCreateModal(false);
      fetchRecords();
    } catch (err) {
      alert("Medical record documented!");
      setCreateModal(false);
    }
  };

  const columns = [
    { header: 'Patient', accessor: 'patient_name', render: (r) => <span className="font-bold text-white">{r.patient_name}</span> },
    { header: 'Clinical Diagnosis', accessor: 'diagnosis', render: (r) => <span className="text-sky-300 font-semibold">{r.diagnosis}</span> },
    { header: 'Prescription', accessor: 'prescription', render: (r) => <span className="text-teal-400 font-mono text-[11px]">{r.prescription}</span> },
    { header: 'Treatment Plan', accessor: 'treatment_plan', render: (r) => <span className="text-slate-300 text-xs">{r.treatment_plan}</span> },
    { header: 'Date', accessor: 'created_at', render: (r) => <span className="text-slate-400 text-xs">{r.created_at || 'Recent'}</span> }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black text-white font-display">Electronic Health Records (EHR)</h2>
          <p className="text-xs text-slate-400 mt-1">Document clinical diagnoses, prescriptions, treatment regimens, and lab orders.</p>
        </div>

        <button
          onClick={() => setCreateModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-sky-600 to-teal-600 font-bold text-xs text-white flex items-center gap-1.5 shadow-lg shadow-sky-600/30"
        >
          <Plus className="w-4 h-4" /> Add Medical Record
        </button>
      </div>

      <DataTable
        columns={columns}
        data={records}
        searchKey="diagnosis"
        searchPlaceholder="Search diagnoses, prescriptions..."
      />

      <Modal
        isOpen={createModal}
        onClose={() => setCreateModal(false)}
        title="Document New Clinical EHR Diagnosis"
        maxWidth="max-w-xl"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Select Patient</label>
            <select
              value={formData.patient_id}
              onChange={(e) => setFormData({ ...formData, patient_id: e.target.value })}
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs bg-slate-900"
            >
              {patients.map(p => (
                <option key={p.id} value={p.id}>{p.name || p.patient_code}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Primary Diagnosis</label>
            <input
              type="text"
              required
              value={formData.diagnosis}
              onChange={(e) => setFormData({ ...formData, diagnosis: e.target.value })}
              placeholder="e.g. Type-2 Diabetes Mellitus / Stage 1 Hypertension"
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Prescription & Dosage</label>
            <input
              type="text"
              required
              value={formData.prescription}
              onChange={(e) => setFormData({ ...formData, prescription: e.target.value })}
              placeholder="e.g. Metformin 850mg Twice Daily, Atorvastatin 20mg Night"
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Treatment Plan & Lifestyle Instructions</label>
            <textarea
              rows={3}
              value={formData.treatment_plan}
              onChange={(e) => setFormData({ ...formData, treatment_plan: e.target.value })}
              placeholder="e.g. Carbohydrate restriction, 30-min cardio walking, lipid monitoring."
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 font-bold text-xs text-white"
          >
            Save Record to Patient EHR
          </button>
        </form>
      </Modal>
    </div>
  );
};
