import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';

export const VitalsChart = ({ vitals = [] }) => {
  // Format vitals for chronological charting
  const chartData = [...vitals].reverse().map((v, i) => ({
    time: v.recorded_at ? new Date(v.recorded_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : `Record #${i+1}`,
    systolic: v.blood_pressure_systolic,
    diastolic: v.blood_pressure_diastolic,
    heart_rate: v.heart_rate,
    spo2: v.spo2,
    glucose: v.blood_glucose || 100
  }));

  if (chartData.length === 0) {
    return (
      <div className="p-12 text-center text-slate-500 text-xs font-semibold">
        No chronological vital trends recorded yet.
      </div>
    );
  }

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 10, right: 20, left: -15, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
          <XAxis dataKey="time" stroke="#94a3b8" fontSize={11} tickLine={false} />
          <YAxis stroke="#94a3b8" fontSize={11} domain={['auto', 'auto']} tickLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', fontSize: '11px', color: '#f8fafc' }}
          />
          <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
          <Line type="monotone" dataKey="systolic" name="Systolic BP (mmHg)" stroke="#f43f5e" strokeWidth={2.5} dot={{ r: 4 }} activeDot={{ r: 6 }} />
          <Line type="monotone" dataKey="diastolic" name="Diastolic BP (mmHg)" stroke="#fb7185" strokeWidth={2} strokeDasharray="4 4" dot={{ r: 3 }} />
          <Line type="monotone" dataKey="heart_rate" name="Heart Rate (BPM)" stroke="#38bdf8" strokeWidth={2} dot={{ r: 4 }} />
          <Line type="monotone" dataKey="spo2" name="SpO2 (%)" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export { RiskGauge } from './RiskGauge';
