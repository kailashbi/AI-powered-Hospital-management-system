import React from 'react';
import { StatCard, Badge } from '../../components/common/StatCard';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid, 
  PieChart, 
  Pie, 
  Cell, 
  Legend 
} from 'recharts';
import { Activity, Brain, Users, FileText } from 'lucide-react';

export const AdminReports = () => {
  const diseaseRiskData = [
    { name: 'Heart Disease', value: 45, color: '#f43f5e' },
    { name: 'Stroke Risk', value: 30, color: '#6366f1' },
    { name: 'Type-2 Diabetes', value: 25, color: '#0d9488' }
  ];

  const patientInflowMonthly = [
    { month: 'Jan', admissions: 42, discharges: 38 },
    { month: 'Feb', admissions: 58, discharges: 52 },
    { month: 'Mar', admissions: 65, discharges: 60 },
    { month: 'Apr', admissions: 78, discharges: 71 },
    { month: 'May', admissions: 92, discharges: 85 },
    { month: 'Jun', admissions: 110, discharges: 102 }
  ];

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h2 className="text-2xl font-black text-white font-display">Hospital Analytics & Predictive Intelligence</h2>
        <p className="text-xs text-slate-400 mt-1">Aggregated clinical reports, AI disease distribution, and patient admission trends.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Patient Inflow vs Discharges */}
        <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white">Patient Inflow & Discharge Rates</h3>
              <p className="text-xs text-slate-400">Monthly patient admission trajectory</p>
            </div>
            <Badge variant="info">Occupancy 78.5%</Badge>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={patientInflowMonthly}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
                <XAxis dataKey="month" stroke="#94a3b8" fontSize={11} tickLine={false} />
                <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px', color: '#fff' }} />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
                <Bar dataKey="admissions" name="Admissions" fill="#0284c7" radius={[4, 4, 0, 0]} />
                <Bar dataKey="discharges" name="Discharges" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Predictive Disease Risk Distribution */}
        <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-white">AI Diagnostic Disease Proportion</h3>
              <p className="text-xs text-slate-400">Distribution of evaluated clinical pathologies</p>
            </div>
            <Badge variant="warning">3 Active ML Models</Badge>
          </div>

          <div className="h-64 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={diseaseRiskData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {diseaseRiskData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px', color: '#fff' }} />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
