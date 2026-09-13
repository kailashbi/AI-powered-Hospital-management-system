import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { User, Mail, Lock, Phone, Calendar, ArrowRight } from 'lucide-react';

export const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    password: '',
    phone: '',
    gender: 'Male',
    date_of_birth: '1995-01-01',
    blood_group: 'O+',
    city: 'New York'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register({ ...formData, role: 'patient' });
      navigate('/patient');
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-xl glass-card rounded-3xl p-8 border border-slate-800 shadow-2xl">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white font-black text-xl shadow-lg shadow-emerald-500/20 mb-2">
            K+
          </div>
          <h2 className="text-2xl font-black text-white font-display">Patient Portal Registration</h2>
          <p className="text-xs text-slate-400 mt-1">Create your personal health record (EHR) and AI health diagnostic account</p>
        </div>

        {/* Notice for Medical Staff */}
        <div className="mb-4 p-3 rounded-2xl bg-sky-950/40 border border-sky-500/30 text-sky-200 text-[11px] leading-relaxed">
          <strong className="text-sky-300 block mb-0.5">ℹ️ Notice for Physicians & Medical Staff:</strong>
          Doctors, Nurses, and Administrative accounts are provisioned and credentialed directly by Hospital Administration. Medical staff should log in with their assigned hospital credentials.
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-semibold">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3.5">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">First Name</label>
              <input type="text" name="first_name" required onChange={handleChange} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Last Name</label>
              <input type="text" name="last_name" required onChange={handleChange} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Username</label>
              <input type="text" name="username" required onChange={handleChange} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Email</label>
              <input type="email" name="email" required onChange={handleChange} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
              <input type="password" name="password" required onChange={handleChange} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Phone Number</label>
              <input type="tel" name="phone" onChange={handleChange} className="w-full glass-input px-3.5 py-2 rounded-xl text-xs" />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Gender</label>
              <select name="gender" onChange={handleChange} className="w-full glass-input px-2 py-2 rounded-xl text-xs bg-slate-900">
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Blood Group</label>
              <select name="blood_group" onChange={handleChange} className="w-full glass-input px-2 py-2 rounded-xl text-xs bg-slate-900">
                <option value="O+">O+</option>
                <option value="A+">A+</option>
                <option value="B+">B+</option>
                <option value="AB+">AB+</option>
                <option value="O-">O-</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Date of Birth</label>
              <input type="date" name="date_of_birth" value={formData.date_of_birth} onChange={handleChange} className="w-full glass-input px-2 py-2 rounded-xl text-xs bg-slate-900" />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-sky-600 to-teal-600 font-bold text-xs text-white shadow-lg shadow-sky-600/30 transition-all flex items-center justify-center gap-2 mt-4"
          >
            {loading ? 'Registering...' : 'Complete Patient Registration'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <div className="text-center mt-6 text-xs text-slate-400">
          Already have an account?{' '}
          <Link to="/login" className="text-sky-400 hover:text-sky-300 font-bold">Sign In</Link>
        </div>
      </div>
    </div>
  );
};

export const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md glass-card rounded-3xl p-8 border border-slate-800 shadow-2xl text-center">
        <h2 className="text-xl font-bold text-white mb-2">Reset Password</h2>
        <p className="text-xs text-slate-400 mb-6">Enter your registered email to receive password reset credentials</p>

        {submitted ? (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-medium">
            ✓ Reset link dispatched. Please check your inbox.
          </div>
        ) : (
          <form onSubmit={(e) => { e.preventDefault(); setSubmitted(true); }} className="space-y-4">
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@kairehealth.com"
              className="w-full glass-input px-4 py-2.5 rounded-xl text-xs"
            />
            <button
              type="submit"
              className="w-full py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 font-bold text-xs text-white"
            >
              Send Instructions
            </button>
          </form>
        )}

        <div className="mt-6 text-xs">
          <Link to="/login" className="text-sky-400 hover:text-sky-300 font-semibold">Back to Login</Link>
        </div>
      </div>
    </div>
  );
};
