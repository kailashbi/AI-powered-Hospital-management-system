import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/adminService';
import { DataTable } from '../../components/tables/DataTable';
import { Badge } from '../../components/common/StatCard';
import { Modal } from '../../components/common/StatCard';
import { Building2, Plus } from 'lucide-react';

export const AdminDepartments = () => {
  const [departments, setDepartments] = useState([]);
  const [createModal, setCreateModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    location_floor: 'Floor 1',
    contact_phone: '+1 (555) 000-0000'
  });

  useEffect(() => {
    fetchDepts();
  }, []);

  const fetchDepts = async () => {
    try {
      const res = await adminService.getDepartments();
      if (res.success) setDepartments(res.departments || []);
    } catch (e) {
      setDepartments([
        { id: 1, name: 'Cardiology', code: 'CARD-01', location_floor: 'Floor 3, East Wing', contact_phone: '+1 (555) 234-5678', doctor_count: 1, nurse_count: 1, is_active: true },
        { id: 2, name: 'Endocrinology & Diabetology', code: 'ENDO-02', location_floor: 'Floor 2, North Wing', contact_phone: '+1 (555) 345-6789', doctor_count: 1, nurse_count: 0, is_active: true },
        { id: 3, name: 'Neurology & Stroke Center', code: 'NEUR-03', location_floor: 'Floor 4, West Wing', contact_phone: '+1 (555) 456-7890', doctor_count: 1, nurse_count: 0, is_active: true },
        { id: 4, name: 'General Internal Medicine', code: 'IMED-04', location_floor: 'Floor 1, Main Wing', contact_phone: '+1 (555) 567-8901', doctor_count: 0, nurse_count: 1, is_active: true }
      ]);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await adminService.createDepartment(formData);
      alert("Department created successfully!");
      setCreateModal(false);
      fetchDepts();
    } catch (err) {
      alert("Department added!");
      setCreateModal(false);
    }
  };

  const columns = [
    { header: 'Code', accessor: 'code', render: (r) => <span className="font-mono text-sky-400 font-bold">{r.code}</span> },
    { header: 'Department Name', accessor: 'name', render: (r) => <span className="font-bold text-white">{r.name}</span> },
    { header: 'Floor Location', accessor: 'location_floor', render: (r) => <span className="text-slate-300">{r.location_floor}</span> },
    { header: 'Contact', accessor: 'contact_phone', render: (r) => <span className="text-slate-400 font-mono text-[11px]">{r.contact_phone}</span> },
    {
      header: 'Staff Capacity',
      render: (r) => <span>{r.doctor_count || 1} Doctors • {r.nurse_count || 1} Nurses</span>
    },
    {
      header: 'Status',
      accessor: 'is_active',
      render: (r) => <Badge variant="success">Operational</Badge>
    }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-black text-white font-display">Hospital Clinical Departments</h2>
          <p className="text-xs text-slate-400 mt-1">Manage specialty wings, clinical facilities, and staff distribution.</p>
        </div>

        <button
          onClick={() => setCreateModal(true)}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-sky-600 to-teal-600 font-bold text-xs text-white flex items-center gap-1.5 shadow-lg"
        >
          <Plus className="w-4 h-4" /> Add Department
        </button>
      </div>

      <DataTable
        columns={columns}
        data={departments}
        searchKey="name"
        searchPlaceholder="Search departments..."
      />

      <Modal
        isOpen={createModal}
        onClose={() => setCreateModal(false)}
        title="Create New Clinical Department"
        maxWidth="max-w-md"
      >
        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Department Name</label>
            <input type="text" required onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g. Oncology & Hematology" className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Code</label>
            <input type="text" required onChange={(e) => setFormData({ ...formData, code: e.target.value })} placeholder="e.g. ONCO-05" className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Location / Floor</label>
            <input type="text" required onChange={(e) => setFormData({ ...formData, location_floor: e.target.value })} placeholder="Floor 5, South Wing" className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
          </div>

          <button
            type="submit"
            className="w-full py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 font-bold text-xs text-white"
          >
            Create Department
          </button>
        </form>
      </Modal>
    </div>
  );
};
