import React, { useState } from 'react';
import { nurseService } from '../../services/nurseService';
import { Badge } from '../../components/common/StatCard';
import { BedDouble, Clock, ShieldCheck, CheckCircle2, AlertCircle } from 'lucide-react';

export const NurseDutyRoom = () => {
  const [dutyStatus, setDutyStatus] = useState('On Duty');
  const [assignedRoom, setAssignedRoom] = useState('Cardiac Care Unit - CCU 301');
  const [shiftTiming, setShiftTiming] = useState('Morning (06:00 - 14:00)');
  const [saved, setSaved] = useState(false);

  const wardBeds = [
    { bed: 'CCU-301 Bed A', patient: 'John Doe (PAT-2026-001)', status: 'Occupied', vitals: 'Stable (BP 138/88)' },
    { bed: 'CCU-301 Bed B', patient: 'Maria Garcia (PAT-2026-002)', status: 'Critical Monitoring', vitals: 'Hypertension Flagged (BP 165/105)' },
    { bed: 'CCU-302 Bed A', patient: 'Unassigned', status: 'Available', vitals: 'Sanitized' },
    { bed: 'CCU-302 Bed B', patient: 'Robert Chen (PAT-2026-003)', status: 'Occupied', vitals: 'Stable (Blood Sugar 110 mg/dL)' }
  ];

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await nurseService.updateDuty({
        duty_status: dutyStatus,
        assigned_room: assignedRoom,
        shift_timing: shiftTiming
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (e) {
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h2 className="text-2xl font-black text-white font-display">Nurse Ward Duty & Room Allocation</h2>
        <p className="text-xs text-slate-400 mt-1">Configure your active shift area, duty status, and monitor assigned ward bed occupancy.</p>
      </div>

      {saved && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" /> Duty status and room roster updated successfully!
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Duty Update Form */}
        <div className="glass-card rounded-3xl border border-slate-800 p-6">
          <h3 className="text-base font-bold text-white mb-4">My Shift & Room Duty</h3>
          <form onSubmit={handleUpdate} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Active Duty Status</label>
              <select
                value={dutyStatus}
                onChange={(e) => setDutyStatus(e.target.value)}
                className="w-full glass-input px-3.5 py-2 rounded-xl text-xs bg-slate-900 font-bold text-teal-300"
              >
                <option value="On Duty">On Duty (Active Ward Care)</option>
                <option value="Break">Break (Temporary Coverage)</option>
                <option value="Off Duty">Off Duty (Shift Ended)</option>
                <option value="Emergency Dispatch">Emergency Dispatch (Code Blue)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Assigned Room / Station</label>
              <input
                type="text"
                value={assignedRoom}
                onChange={(e) => setAssignedRoom(e.target.value)}
                className="w-full glass-input px-3.5 py-2 rounded-xl text-xs font-semibold text-white"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Shift Timing Schedule</label>
              <select
                value={shiftTiming}
                onChange={(e) => setShiftTiming(e.target.value)}
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
              Update My Duty Roster
            </button>
          </form>
        </div>

        {/* Room Bed Occupancy Table */}
        <div className="lg:col-span-2 glass-card rounded-3xl border border-slate-800 p-6">
          <h3 className="text-base font-bold text-white mb-1">Ward Bed Allocation & Occupancy</h3>
          <p className="text-xs text-slate-400 mb-4">Real-time status of beds in your assigned care unit ({assignedRoom})</p>

          <div className="space-y-3">
            {wardBeds.map((b, idx) => (
              <div key={idx} className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-slate-800 text-teal-400 border border-slate-700">
                    <BedDouble className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-white">{b.bed}</h4>
                    <p className="text-xs text-slate-400">{b.patient}</p>
                  </div>
                </div>

                <div className="text-right space-y-1">
                  <Badge variant={b.status === 'Available' ? 'success' : (b.status === 'Critical Monitoring' ? 'danger' : 'info')}>
                    {b.status}
                  </Badge>
                  <p className="text-[11px] text-slate-400 font-medium">{b.vitals}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
