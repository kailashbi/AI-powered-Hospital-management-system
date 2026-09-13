import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { 
  Lock, 
  Mail, 
  Sparkles, 
  ShieldCheck, 
  Stethoscope, 
  HeartPulse, 
  User, 
  ArrowRight,
  Activity,
  Check,
  Zap,
  KeyRound,
  Layers
} from 'lucide-react';

export const Login = () => {
  const navigate = useNavigate();
  const { login, quickSwitch } = useAuth();
  const [email, setEmail] = useState('dr.ankit@kairehealth.com');
  const [password, setPassword] = useState('password123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all'); // 'all', 'doctor', 'nurse', 'patient', 'admin'
  const [activePersonaKey, setActivePersonaKey] = useState('doctor_sarah');

  // Complete List of All Demo Personas across all 4 Hospital Roles
  const demoPersonas = [
    {
      id: 'doctor_sarah',
      role: 'doctor',
      category: 'doctor',
      name: 'Dr. Ankit',
      title: 'Interventional Cardiologist',
      department: 'Cardiology (Floor 3)',
      email: 'dr.ankit@kairehealth.com',
      avatar: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150',
      icon: Stethoscope,
      accent: 'border-sky-500/40 bg-sky-950/30 text-sky-400',
      badgeColor: 'bg-sky-500/20 text-sky-300 border-sky-500/30',
      description: 'Cardiac risk evaluation, ECG assessment & AI Heart Disease models'
    },
    {
      id: 'doctor_alex',
      role: 'doctor',
      category: 'doctor',
      name: 'Dr. Rawtaram',
      title: 'Endocrinologist & Metabolism',
      department: 'Endocrinology (Floor 2)',
      email: 'dr.rawtaram@kairehealth.com',
      avatar: 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150',
      icon: Activity,
      accent: 'border-teal-500/40 bg-teal-950/30 text-teal-400',
      badgeColor: 'bg-teal-500/20 text-teal-300 border-teal-500/30',
      description: 'Type-2 diabetes diagnostics, insulin titration & metabolic panels'
    },
    {
      id: 'doctor_elena',
      role: 'doctor',
      category: 'doctor',
      name: 'Dr. Amit',
      title: 'Vascular Neurologist',
      department: 'Neurology & Stroke (Floor 4)',
      email: 'dr.amit@kairehealth.com',
      avatar: 'https://images.unsplash.com/photo-1594824813689-f53e6b72a0f8?w=150',
      icon: Zap,
      accent: 'border-indigo-500/40 bg-indigo-950/30 text-indigo-400',
      badgeColor: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30',
      description: 'Acute stroke risk stratification & neuro-rehab monitoring'
    },
    {
      id: 'nurse_emily',
      role: 'nurse',
      category: 'nurse',
      name: 'Nurse Sunder',
      title: 'Critical Care / ICU Nurse',
      department: 'Cardiac Care Unit (CCU 301)',
      email: 'nurse.sunder@kairehealth.com',
      avatar: 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=150',
      icon: HeartPulse,
      accent: 'border-teal-500/40 bg-teal-950/30 text-teal-400',
      badgeColor: 'bg-teal-500/20 text-teal-300 border-teal-500/30',
      description: 'Triage vitals logging, abnormal alert triggering & duty management'
    },
    {
      id: 'nurse_marcus',
      role: 'nurse',
      category: 'nurse',
      name: 'Nurse Dholi',
      title: 'Emergency Care Specialist',
      department: 'Emergency & General Ward (Rooms 201-208)',
      email: 'nurse.dholi@kairehealth.com',
      avatar: 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150',
      icon: HeartPulse,
      accent: 'border-cyan-500/40 bg-cyan-950/30 text-cyan-400',
      badgeColor: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
      description: 'Trauma triage, inpatient vital monitoring & shift handover'
    },
    {
      id: 'patient_john',
      role: 'patient',
      category: 'patient',
      name: 'Mukesh',
      title: 'Patient (PAT-2026-001)',
      department: 'Room 301-Bed A',
      email: 'mukesh@gmail.com',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150',
      icon: User,
      accent: 'border-emerald-500/40 bg-emerald-950/30 text-emerald-400',
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
      description: 'Cardiovascular risk profile, cardiology appointments & prescriptions'
    },
    {
      id: 'patient_maria',
      role: 'patient',
      category: 'patient',
      name: 'Yanshu',
      title: 'Patient (PAT-2026-002)',
      department: 'Room 408-Bed B',
      email: 'yanshu@gmail.com',
      avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150',
      icon: User,
      accent: 'border-emerald-500/40 bg-emerald-950/30 text-emerald-400',
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
      description: 'Stroke risk profile, neurology consults & blood pressure telemetry'
    },
    {
      id: 'patient_robert',
      role: 'patient',
      category: 'patient',
      name: 'Robert Chen',
      title: 'Patient (PAT-2026-003)',
      department: 'Outpatient Clinic',
      email: 'robert.chen@gmail.com',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150',
      icon: User,
      accent: 'border-emerald-500/40 bg-emerald-950/30 text-emerald-400',
      badgeColor: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
      description: 'Type-2 diabetes management, HbA1c tracking & diet monitoring'
    },
    {
      id: 'admin_arthur',
      role: 'admin',
      category: 'admin',
      name: 'Kailash Admin',
      title: 'Chief System Administrator',
      department: 'Hospital HQ Executive Suite',
      email: 'admin@kairehealth.com',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150',
      icon: ShieldCheck,
      accent: 'border-rose-500/40 bg-rose-950/30 text-rose-400',
      badgeColor: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
      description: 'Hospital overview, doctor/nurse roster, audit logs & system settings'
    }
  ];

  const filteredPersonas = selectedCategory === 'all' 
    ? demoPersonas 
    : demoPersonas.filter(p => p.category === selectedCategory);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await login(email, password);
      redirectRole(user.role);
    } catch (err) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = async (persona) => {
    setError('');
    setActivePersonaKey(persona.id);
    setLoading(true);
    try {
      const user = await quickSwitch(persona.id);
      redirectRole(user.role || persona.role);
    } catch (err) {
      setError('Demo switch failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAutofill = (persona) => {
    setEmail(persona.email);
    setPassword('password123');
    setActivePersonaKey(persona.id);
    setError('');
  };

  const redirectRole = (role) => {
    switch (role) {
      case 'admin': navigate('/admin'); break;
      case 'doctor': navigate('/doctor'); break;
      case 'nurse': navigate('/nurse'); break;
      case 'patient': navigate('/patient'); break;
      default: navigate('/doctor'); break;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 sm:p-6 lg:p-10 relative overflow-hidden">
      {/* Ambient Gradient Glows */}
      <div className="absolute -top-40 -left-40 w-[32rem] h-[32rem] bg-sky-500/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-[32rem] h-[32rem] bg-teal-500/15 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[40rem] h-[40rem] bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-5xl glass-card rounded-3xl p-6 sm:p-8 lg:p-10 border border-slate-800/90 shadow-2xl relative z-10 animate-scaleUp">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-sky-600 via-teal-500 to-indigo-600 text-white font-black text-2xl shadow-xl shadow-sky-500/25 mb-3">
            K+
          </div>
          <h1 className="text-3xl lg:text-4xl font-black text-white tracking-tight font-display">
            KAIre <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-teal-300">Health</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-md mx-auto">
            Next-Gen AI Hospital Management & Clinical Diagnostic Intelligence
          </p>
        </div>

        {/* 1-Click Fast Demo Login Hub */}
        <div className="mb-8 p-5 rounded-2xl bg-slate-900/90 border border-slate-800/90 shadow-inner">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-sky-500/20 text-sky-400">
                <Sparkles className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs sm:text-sm font-black uppercase tracking-wider text-slate-100 flex items-center gap-2">
                  1-Click Demo Login & Role Hub
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-bold lowercase">
                    all roles available
                  </span>
                </h3>
                <p className="text-[11px] text-slate-400">Select any clinical role or persona to sign in instantly or auto-fill credentials.</p>
              </div>
            </div>

            {/* Role Filter Tabs */}
            <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
              {[
                { key: 'all', label: 'All Roles' },
                { key: 'doctor', label: 'Doctors' },
                { key: 'nurse', label: 'Nurses' },
                { key: 'patient', label: 'Patients' },
                { key: 'admin', label: 'Admin' }
              ].map(tab => (
                <button
                  key={tab.key}
                  type="button"
                  onClick={() => setSelectedCategory(tab.key)}
                  className={`px-2.5 py-1 rounded-lg font-bold text-[11px] transition-all ${
                    selectedCategory === tab.key
                      ? 'bg-sky-600 text-white shadow-md shadow-sky-600/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Demo Persona Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[360px] overflow-y-auto pr-1">
            {filteredPersonas.map((persona) => {
              const Icon = persona.icon;
              const isSelected = activePersonaKey === persona.id;

              return (
                <div
                  key={persona.id}
                  className={`p-3.5 rounded-2xl border transition-all duration-200 flex flex-col justify-between group ${
                    isSelected
                      ? 'border-sky-500 bg-sky-950/40 shadow-lg shadow-sky-500/10 ring-1 ring-sky-500/50'
                      : 'border-slate-800 bg-slate-950/70 hover:border-slate-700 hover:bg-slate-900/80'
                  }`}
                >
                  <div>
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2.5">
                        <img 
                          src={persona.avatar} 
                          alt={persona.name}
                          className="w-10 h-10 rounded-xl object-cover border border-slate-700 shadow-sm"
                        />
                        <div>
                          <div className="flex items-center gap-1.5">
                            <span className="text-xs font-black text-white leading-tight">{persona.name}</span>
                          </div>
                          <span className="text-[10px] text-slate-400 block">{persona.title}</span>
                        </div>
                      </div>
                      <span className={`text-[9px] font-extrabold px-2 py-0.5 rounded-full border uppercase tracking-wider ${persona.badgeColor}`}>
                        {persona.role}
                      </span>
                    </div>

                    <p className="text-[11px] text-slate-400 line-clamp-2 mb-3 leading-relaxed">
                      {persona.description}
                    </p>
                  </div>

                  <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between gap-2">
                    <button
                      type="button"
                      onClick={() => handleAutofill(persona)}
                      className="px-2.5 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-[10px] font-bold text-slate-300 border border-slate-700/80 flex items-center gap-1 transition-colors"
                      title="Auto-fill email and password into standard form"
                    >
                      <KeyRound className="w-3 h-3 text-sky-400" />
                      Auto-Fill
                    </button>

                    <button
                      type="button"
                      disabled={loading}
                      onClick={() => handleQuickDemo(persona)}
                      className="flex-1 px-3 py-1.5 rounded-xl bg-gradient-to-r from-sky-600 to-teal-600 hover:from-sky-500 hover:to-teal-500 text-[11px] font-black text-white shadow-md shadow-sky-600/25 flex items-center justify-center gap-1.5 transition-all disabled:opacity-50"
                    >
                      <Zap className="w-3 h-3 fill-white" />
                      1-Click Sign In
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-rose-400 animate-ping" />
            {error}
          </div>
        )}

        {/* Standard Email / Password Form */}
        <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80">
          <div className="flex items-center gap-2 mb-4">
            <Lock className="w-4 h-4 text-sky-400" />
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-300">
              Standard Credentials Authentication
            </h4>
          </div>

          <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">Email or Username</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="doctor@kairehealth.com"
                  className="w-full glass-input pl-10 pr-4 py-2.5 rounded-xl text-xs bg-slate-950"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-xs font-semibold text-slate-300">Password</label>
                <Link to="/forgot-password" className="text-[11px] text-sky-400 hover:text-sky-300 font-medium">Forgot?</Link>
              </div>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full glass-input pl-10 pr-4 py-2.5 rounded-xl text-xs bg-slate-950"
                />
              </div>
            </div>

            <div className="sm:col-span-2 pt-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-xl bg-gradient-to-r from-sky-600 via-teal-600 to-indigo-600 hover:from-sky-500 hover:via-teal-500 hover:to-indigo-500 font-black text-xs text-white shadow-lg shadow-sky-600/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? 'Authenticating Clinical Credentials...' : 'Sign In with Entered Credentials'}
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </form>
        </div>

        {/* Footer info */}
        <div className="text-center mt-6 pt-4 border-t border-slate-800 text-xs text-slate-400 space-y-1.5">
          <p>
            Need a new patient portal account?{' '}
            <Link to="/register" className="text-sky-400 hover:text-sky-300 font-bold underline underline-offset-4">
              Register as Patient
            </Link>
          </p>
          <p className="text-[11px] text-slate-500">
            Password for all demo accounts: <code className="text-sky-400 font-mono font-bold bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800">password123</code>
          </p>
        </div>
      </div>
    </div>
  );
};

