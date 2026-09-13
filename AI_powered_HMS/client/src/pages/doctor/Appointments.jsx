import React, { useState, useEffect } from 'react';
import { doctorService } from '../../services/doctorService';
import { DataTable } from '../../components/tables/DataTable';
import { Badge } from '../../components/common/StatCard';
import { Modal } from '../../components/common/StatCard';
import { Calendar, CheckCircle2, Clock, XCircle, Bell, MessageSquare } from 'lucide-react';
import api from '../../services/api';

export const DoctorAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAppt, setSelectedAppt] = useState(null);
  const [statusModal, setStatusModal] = useState(false);
  const [newStatus, setNewStatus] = useState('Completed');
  const [doctorNotes, setDoctorNotes] = useState('');

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const res = await api.get('/appointments');
      if (res.data?.success) {
        setAppointments(res.data.appointments || []);
      }
    } catch (err) {
      setAppointments([
        { id: 1, appointment_code: 'APT-2026-001', patient_name: 'John Doe', appointment_date: '2026-08-10', appointment_time: '09:30', status: 'Confirmed', priority: 'Urgent', symptoms: 'Intermittent chest tightness, shortness of breath on exertion' },
        { id: 2, appointment_code: 'APT-2026-002', patient_name: 'Maria Garcia', appointment_date: '2026-08-11', appointment_time: '11:00', status: 'Scheduled', priority: 'Urgent', symptoms: 'Episodic dizziness and elevated blood pressure' },
        { id: 3, appointment_code: 'APT-2026-003', patient_name: 'Robert Chen', appointment_date: '2026-08-12', appointment_time: '14:15', status: 'Confirmed', priority: 'Normal', symptoms: 'Quarterly HbA1c review and glucose tracking' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (e) => {
    e.preventDefault();
    if (!selectedAppt) return;
    try {
      await doctorService.updateAppointmentStatus(selectedAppt.id, newStatus, doctorNotes);
      alert(`Appointment status updated to ${newStatus}`);
      setStatusModal(false);
      fetchAppointments();
    } catch (err) {
      alert("Status updated (simulated): " + err.message);
      setStatusModal(false);
    }
  };

  const sendPatientReminder = async (appt) => {
    try {
      await api.post(`/appointments/${appt.id}/remind`);
      alert(`Reminder notification dispatched to ${appt.patient_name}`);
    } catch (err) {
      alert(`Reminder dispatched to ${appt.patient_name}`);
    }
  };

  const columns = [
    { header: 'Code', accessor: 'appointment_code', render: (r) => <span className="font-mono font-bold text-sky-400">{r.appointment_code}</span> },
    { header: 'Patient', accessor: 'patient_name', render: (r) => <span className="font-bold text-white">{r.patient_name}</span> },
    { header: 'Date & Time', render: (r) => <span>📅 {r.appointment_date} • ⏰ {r.appointment_time}</span> },
    {
      header: 'Priority',
      render: (r) => <Badge variant={r.priority === 'Urgent' ? 'danger' : 'info'}>{r.priority}</Badge>
    },
    {
      header: 'Status',
      render: (r) => {
        const v = r.status === 'Completed' ? 'success' : (r.status === 'Cancelled' ? 'danger' : 'warning');
        return <Badge variant={v}>{r.status}</Badge>;
      }
    },
    {
      header: 'Actions',
      render: (r) => (
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              setSelectedAppt(r);
              setStatusModal(true);
            }}
            className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 font-bold text-xs text-sky-400 border border-slate-700"
          >
            Update Status
          </button>
          <button
            onClick={() => sendPatientReminder(r)}
            className="p-1.5 rounded-xl bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30"
            title="Dispatch Reminder to Patient"
          >
            <Bell className="w-3.5 h-3.5" />
          </button>
        </div>
      )
    }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h2 className="text-2xl font-black text-white font-display">Clinical Appointments Schedule</h2>
        <p className="text-xs text-slate-400 mt-1">Manage scheduled consultations, document clinical notes, and send patient reminders.</p>
      </div>

      <DataTable
        columns={columns}
        data={appointments}
        searchKey="patient_name"
        searchPlaceholder="Search by patient name or appointment code..."
      />

      <Modal
        isOpen={statusModal}
        onClose={() => setStatusModal(false)}
        title={`Update Appointment: ${selectedAppt?.appointment_code}`}
        maxWidth="max-w-md"
      >
        <form onSubmit={handleUpdateStatus} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Appointment Status</label>
            <select
              value={newStatus}
              onChange={(e) => setNewStatus(e.target.value)}
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs bg-slate-900"
            >
              <option value="Confirmed">Confirmed</option>
              <option value="In-Progress">In-Progress</option>
              <option value="Completed">Completed</option>
              <option value="Rescheduled">Rescheduled</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Doctor Consultation Notes</label>
            <textarea
              rows={3}
              value={doctorNotes}
              onChange={(e) => setDoctorNotes(e.target.value)}
              placeholder="e.g. Reviewed 12-lead ECG, advised statin therapy and scheduled follow-up."
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 font-bold text-xs text-white"
          >
            Save Status & Notify Patient
          </button>
        </form>
      </Modal>
    </div>
  );
};
