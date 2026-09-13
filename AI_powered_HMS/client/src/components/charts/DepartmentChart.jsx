import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';

export const DepartmentChart = ({ departments = [] }) => {
  const data = departments.map(d => ({
    name: d.name.split(' ')[0], // short name
    doctors: d.doctors || d.doctor_count || 1,
    nurses: d.nurses || d.nurse_count || 2,
    appointments: d.appointments || 4
  }));

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 15, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
          <XAxis dataKey="name" stroke="#94a3b8" fontSize={10} tickLine={false} />
          <YAxis stroke="#94a3b8" fontSize={10} tickLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px', color: '#f8fafc' }}
          />
          <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
          <Bar dataKey="appointments" name="Patient Volume" fill="#0284c7" radius={[6, 6, 0, 0]} />
          <Bar dataKey="doctors" name="Physicians" fill="#0d9488" radius={[6, 6, 0, 0]} />
          <Bar dataKey="nurses" name="Nurses" fill="#6366f1" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
