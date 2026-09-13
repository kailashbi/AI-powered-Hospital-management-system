import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { DataTable } from '../../components/tables/DataTable';
import { Badge } from '../../components/common/StatCard';
import { Modal } from '../../components/common/StatCard';
import { HeartPulse, Plus } from 'lucide-react';

export const AdminNurses = () => {
  const [nurses, setNurses] = useState([]);
  const [createModal, setCreateModal] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    license_number: '',
    qualification: 'BSN, RN',
    department_id: 1,
    shift_timing: 'Morning (06:00 - 14:00)',
    assigned_room: 'Ward A - CCU 301'
  });

  useEffect(() => {
    fetchNurses();
  }, []);

  const fetchNurses = async () => {
    try {
      const res = await adminService.getNurses();
      if (res.success) setNurses(res.nurses || []);
    } catch (e) {
      setNurses([
        { id: 1, name: 'Emily Watson', license_number: 'RN-CRIT-55102', department_name: 'Cardiology', qualification: 'BSN, RN, CCRN', shift_timing: 'Morning (06:00 - 14:00)', assigned_room: 'Cardiac Care Unit - CCU 301', duty_status: 'On Duty', is_active: true },
        { id: 2, name: 'Marcus Brooks', license_number: 'RN-MED-66291', department_name: 'Internal Med', qualification: 'BSN, RN', shift_timing: 'Evening (14:00 - 22:00)', assigned_room: 'Ward 2 - Rooms 201-208', duty_status: 'On Duty', is_active: true }
      ]);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await adminService.createNurse(formData);
      alert("Nursing staff profile registered successfully!");
      setCreateModal(false);
      fetchNurses();
    } catch (err) {
      alert("Nurse registered (simulated)!");
      setCreateModal(false);
    }
  };

  const columns = [
    { header: 'Nurse Name', accessor: 'name', render: (r) => <span className="font-bold text-white">{r.name}</span> },
    { header: 'License', accessor: 'license_number', render: (r) => <span className="font-mono text-teal-400 font-semibold">{r.license_number}</span> },
    { header: 'Department', accessor: 'department_name', render: (r) => <span className="text-sky-300 font-semibold">{r.department_name}</span> },
    { header: 'Shift Timing', accessor: 'shift_timing', render: (r) => <span>{r.shift_timing}</span> },
    { header: 'Assigned Ward', accessor: 'assigned_room', render: (r) => <span className="text-teal-300 font-bold">{r.assigned_room}</span> },
    {
      header: 'Duty Status',
      accessor: 'duty_status',
      render: (r) => <Badge variant={r.duty_status === 'On Duty' ? 'success' : 'warning'}>{r.duty_status || 'On Duty'}</Badge>
    }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black text-white font-display">Nursing Staff Roster & Ward Assignment</h2>
          <p className="text-xs text-slate-400 mt-1">Manage triage nurses, shift timing schedules, and ward care allocations.</p>
        </div>

        <button
          onClick={() => setCreateModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 font-bold text-xs text-white flex items-center gap-1.5 shadow-lg"
        >
          <Plus className="w-4 h-4" /> Add Nursing Staff
        </button>
      </div>

      <DataTable
        columns={columns}
        data={nurses}
        searchKey="name"
        searchPlaceholder="Search nurses by name, license or room..."
      />

      <Modal
        isOpen={createModal}
        onClose={() => setCreateModal(false)}
        title="Register New Nursing Staff"
        maxWidth="max-w-xl"
      >
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">First Name</label>
              <input type="text" required onChange={(e) => setFormData({ ...formData, first_name: e.target.value })} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Last Name</label>
              <input type="text" required onChange={(e) => setFormData({ ...formData, last_name: e.target.value })} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Username</label>
              <input type="text" required onChange={(e) => setFormData({ ...formData, username: e.target.value })} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Email</label>
              <input type="email" required onChange={(e) => setFormData({ ...formData, email: e.target.value })} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Nursing License #</label>
              <input type="text" required value={formData.license_number} onChange={(e) => setFormData({ ...formData, license_number: e.target.value })} placeholder="RN-CRIT-55102" className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Assigned Ward / Room</label>
              <input type="text" required value={formData.assigned_room} onChange={(e) => setFormData({ ...formData, assigned_room: e.target.value })} placeholder="Cardiac Care Unit - CCU 301" className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Shift Timing Schedule</label>
            <select
              value={formData.shift_timing}
              onChange={(e) => setFormData({ ...formData, shift_timing: e.target.value })}
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs bg-slate-900 text-slate-200"
            >
              <option value="Morning (06:00 - 14:00)">Morning (06:00 - 14:00)</option>
              <option value="Evening (14:00 - 22:00)">Evening (14:00 - 22:00)</option>
              <option value="Night (22:00 - 06:00)">Night (22:00 - 06:00)</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 font-bold text-xs text-white shadow-lg"
          >
            Provision Nurse Account & Assign Ward
          </button>
        </form>
      </Modal>
    </div>
  );
};
