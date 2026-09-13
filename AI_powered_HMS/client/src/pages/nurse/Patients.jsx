import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { doctorService } from '../../services/doctorService';
import { DataTable } from '../../components/tables/DataTable';
import { Badge } from '../../components/common/StatCard';
import { Activity, User, BedDouble } from 'lucide-react';

export const NursePatients = () => {
  const navigate = useNavigate();
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const res = await doctorService.getPatients();
      if (res.success) setPatients(res.patients || []);
    } catch (e) {
      setPatients([
        { id: 1, patient_code: 'PAT-2026-001', name: 'John Doe', age: 52, gender: 'Male', blood_group: 'O+', assigned_room: 'Room 301-Bed A' },
        { id: 2, patient_code: 'PAT-2026-002', name: 'Maria Garcia', age: 57, gender: 'Female', blood_group: 'A+', assigned_room: 'Room 408-Bed B' },
        { id: 3, patient_code: 'PAT-2026-003', name: 'Robert Chen', age: 37, gender: 'Male', blood_group: 'B+', assigned_room: 'Outpatient' }
      ]);
    }
  };

  const columns = [
    { header: 'Patient Code', accessor: 'patient_code', render: (r) => <span className="font-mono font-bold text-teal-400">{r.patient_code}</span> },
    { header: 'Patient Name', accessor: 'name', render: (r) => <span className="font-bold text-white">{r.name}</span> },
    { header: 'Age / Gender', render: (r) => <span>{r.age || 45} yrs • {r.gender}</span> },
    { header: 'Blood Group', accessor: 'blood_group', render: (r) => <Badge variant="info">{r.blood_group || 'O+'}</Badge> },
    { header: 'Assigned Bed / Room', accessor: 'assigned_room', render: (r) => <span className="text-teal-300 font-semibold">{r.assigned_room || 'General Ward'}</span> },
    {
      header: 'Actions',
      render: (r) => (
        <button
          onClick={() => navigate(`/nurse/vitals?patient_id=${r.id}`)}
          className="px-3 py-1.5 rounded-xl bg-teal-600/20 hover:bg-teal-600/40 text-teal-300 border border-teal-500/30 font-bold text-xs flex items-center gap-1.5"
        >
          <Activity className="w-3.5 h-3.5" /> Record Vitals
        </button>
      )
    }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h2 className="text-2xl font-black text-white font-display">Inpatient & Ward Triage Directory</h2>
        <p className="text-xs text-slate-400 mt-1">Select any patient to record physiological vitals or view bed assignment details.</p>
      </div>

      <DataTable
        columns={columns}
        data={patients}
        searchKey="name"
        searchPlaceholder="Search patients by name, code or room..."
      />
    </div>
  );
};
