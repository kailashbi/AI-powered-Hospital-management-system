import React, { useState, useEffect } from 'react';
import { patientService } from '../../services/patientService';
import { DataTable } from '../../components/tables/DataTable';
import { Badge } from '../../components/common/StatCard';
import { Modal } from '../../components/common/StatCard';
import { Calendar, Plus, CheckCircle2 } from 'lucide-react';
import api from '../../services/api';

export const PatientAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [bookModal, setBookModal] = useState(false);
  const [doctors, setDoctors] = useState([]);
  const [formData, setFormData] = useState({
    doctor_id: '1',
    department_id: '1',
    appointment_date: new Date(Date.now() + 86400000 * 2).toISOString().split('T')[0],
    appointment_time: '10:00',
    symptoms: '',
    priority: 'Normal'
  });

  useEffect(() => {
    fetchAppointments();
    fetchDoctors();
  }, []);

  const fetchAppointments = async () => {
    try {
      const res = await patientService.getAppointments();
      if (res.success) setAppointments(res.appointments || []);
    } catch (e) {
      setAppointments([
        { id: 1, appointment_code: 'APT-2026-001', doctor_name: 'Dr. Sarah Chen', department_name: 'Cardiology', appointment_date: '2026-08-10', appointment_time: '09:30', status: 'Confirmed', priority: 'Urgent', symptoms: 'Intermittent chest tightness, shortness of breath on exertion' }
      ]);
    }
  };

  const fetchDoctors = async () => {
    try {
      const res = await api.get('/admin/doctors');
      if (res.data?.success) setDoctors(res.data.doctors || []);
    } catch (e) {
      setDoctors([
        { id: 1, name: 'Dr. Sarah Chen', specialization: 'Interventional Cardiology', department_id: 1 },
        { id: 2, name: 'Dr. Alex Reyes', specialization: 'Endocrinology & Metabolism', department_id: 2 },
        { id: 3, name: 'Dr. Elena Rostova', specialization: 'Vascular Neurology & Stroke', department_id: 3 }
      ]);
    }
  };

  const handleBook = async (e) => {
    e.preventDefault();
    try {
      await patientService.bookAppointment(formData);
      alert("Appointment consultation requested successfully!");
      setBookModal(false);
      fetchAppointments();
    } catch (err) {
      alert("Consultation scheduled (simulated)!");
      setBookModal(false);
    }
  };

  const columns = [
    { header: 'Code', accessor: 'appointment_code', render: (r) => <span className="font-mono font-bold text-sky-400">{r.appointment_code}</span> },
    { header: 'Attending Doctor', accessor: 'doctor_name', render: (r) => <span className="font-bold text-white">{r.doctor_name}</span> },
    { header: 'Department', accessor: 'department_name', render: (r) => <span className="text-teal-400 font-semibold">{r.department_name}</span> },
    { header: 'Scheduled Slot', render: (r) => <span>📅 {r.appointment_date} • ⏰ {r.appointment_time}</span> },
    { header: 'Priority', render: (r) => <Badge variant={r.priority === 'Urgent' ? 'danger' : 'info'}>{r.priority}</Badge> },
    { header: 'Status', render: (r) => <Badge variant={r.status === 'Confirmed' ? 'success' : 'warning'}>{r.status}</Badge> }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black text-white font-display">My Clinical Appointments</h2>
          <p className="text-xs text-slate-400 mt-1">Book new doctor consultations, view status updates, and review preparation instructions.</p>
        </div>

        <button
          onClick={() => setBookModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 font-bold text-xs text-white flex items-center gap-1.5 shadow-lg"
        >
          <Plus className="w-4 h-4" /> Book Appointment
        </button>
      </div>

      <DataTable
        columns={columns}
        data={appointments}
        searchKey="doctor_name"
        searchPlaceholder="Search by doctor or appointment code..."
      />

      <Modal
        isOpen={bookModal}
        onClose={() => setBookModal(false)}
        title="Schedule Physician Consultation"
        maxWidth="max-w-lg"
      >
        <form onSubmit={handleBook} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Select Physician & Specialization</label>
            <select
              value={formData.doctor_id}
              onChange={(e) => {
                const doc = doctors.find(d => String(d.id) === e.target.value);
                setFormData({
                  ...formData,
                  doctor_id: e.target.value,
                  department_id: doc ? String(doc.department_id) : '1'
                });
              }}
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs bg-slate-900 font-semibold"
            >
              {doctors.map(d => (
                <option key={d.id} value={d.id}>
                  {d.name} — {d.specialization}
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Date</label>
              <input
                type="date"
                required
                value={formData.appointment_date}
                onChange={(e) => setFormData({ ...formData, appointment_date: e.target.value })}
                className="w-full glass-input px-3 py-2 rounded-xl text-xs bg-slate-900"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Time Slot</label>
              <select
                value={formData.appointment_time}
                onChange={(e) => setFormData({ ...formData, appointment_time: e.target.value })}
                className="w-full glass-input px-3 py-2 rounded-xl text-xs bg-slate-900"
              >
                <option value="09:00">09:00 AM</option>
                <option value="09:30">09:30 AM</option>
                <option value="11:00">11:00 AM</option>
                <option value="14:15">02:15 PM</option>
                <option value="16:00">04:00 PM</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Current Symptoms & Primary Concern</label>
            <textarea
              rows={3}
              required
              value={formData.symptoms}
              onChange={(e) => setFormData({ ...formData, symptoms: e.target.value })}
              placeholder="Describe your symptoms (e.g. chest pressure on exertion, fasting glucose elevation, etc.)"
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 font-bold text-xs text-white"
          >
            Confirm Appointment Request
          </button>
        </form>
      </Modal>
    </div>
  );
};
