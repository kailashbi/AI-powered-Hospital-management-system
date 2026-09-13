import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { User, Phone, Mail, Shield, AlertCircle, Heart, MapPin, Calendar } from 'lucide-react';

export const PatientProfile = () => {
  const { user } = useAuth();

  const profile = {
    patient_code: 'PAT-2026-001',
    first_name: user?.first_name || 'John',
    last_name: user?.last_name || 'Doe',
    email: user?.email || 'john.doe@gmail.com',
    phone: '+1 (555) 400-0007',
    date_of_birth: '1974-05-14 (52 yrs)',
    gender: 'Male',
    blood_group: 'O+',
    marital_status: 'Married',
    address: '742 Evergreen Terrace, Springfield, IL',
    insurance_provider: 'Blue Cross Blue Shield (Policy: BCBS-99882211)',
    allergies: 'Penicillin, Shellfish',
    emergency_contact: 'Jane Doe (Wife) - +1 (555) 444-1234',
    attending_physician: 'Dr. Sarah Chen (Cardiology - Room 304-A)'
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h2 className="text-2xl font-black text-white font-display">Patient Health Profile & Demographics</h2>
        <p className="text-xs text-slate-400 mt-1">Verified medical insurance, emergency contacts, allergy alerts, and assigned clinical care team.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Profile Summary Card */}
        <div className="glass-card rounded-3xl border border-slate-800 p-6 flex flex-col items-center text-center">
          <img
            src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200"
            alt="Patient"
            className="w-24 h-24 rounded-3xl object-cover border-2 border-emerald-500/40 shadow-xl mb-4"
          />
          <h3 className="text-lg font-bold text-white">{profile.first_name} {profile.last_name}</h3>
          <span className="font-mono text-xs font-extrabold text-sky-400 mt-0.5">{profile.patient_code}</span>
          <span className="px-3 py-1 rounded-full text-[11px] font-bold bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 mt-3">
            Active Outpatient / Inpatient
          </span>

          <div className="w-full mt-6 pt-6 border-t border-slate-800 space-y-3 text-xs text-left">
            <div className="flex items-center justify-between text-slate-300">
              <span className="text-slate-500">Blood Group:</span>
              <strong className="text-white font-bold">{profile.blood_group}</strong>
            </div>
            <div className="flex items-center justify-between text-slate-300">
              <span className="text-slate-500">Age:</span>
              <strong className="text-white font-bold">{profile.date_of_birth}</strong>
            </div>
            <div className="flex items-center justify-between text-slate-300">
              <span className="text-slate-500">Gender:</span>
              <strong className="text-white font-bold">{profile.gender}</strong>
            </div>
          </div>
        </div>

        {/* Right Details Grid */}
        <div className="lg:col-span-2 glass-card rounded-3xl border border-slate-800 p-6 space-y-6">
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Clinical Care Team & Location</h4>
            <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs space-y-2">
              <div><strong className="text-slate-400">Attending Physician:</strong> <span className="text-sky-300 font-bold">{profile.attending_physician}</span></div>
              <div><strong className="text-slate-400">Residential Address:</strong> <span className="text-slate-200">{profile.address}</span></div>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-rose-400 mb-3">Allergy & Drug Sensitivity Alerts</h4>
            <div className="p-4 rounded-2xl bg-rose-950/20 border border-rose-500/30 text-xs">
              <span className="font-bold text-rose-300">{profile.allergies}</span>
              <p className="text-[11px] text-slate-400 mt-1">Flagged in pharmacy dispensing system. Avoid beta-lactam antibiotics.</p>
            </div>
          </div>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-teal-400 mb-3">Medical Insurance & Emergency Contact</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase font-bold">Insurance Provider</span>
                <span className="font-bold text-white">{profile.insurance_provider}</span>
              </div>
              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
                <span className="text-slate-500 block text-[10px] uppercase font-bold">Emergency Contact</span>
                <span className="font-bold text-white">{profile.emergency_contact}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
