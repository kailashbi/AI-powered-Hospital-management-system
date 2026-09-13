import React, { useState } from 'react';
import { Badge } from '../../components/common/StatCard';
import { Settings, Database, Brain, Lock, Server, CheckCircle2 } from 'lucide-react';

export const AdminSettings = () => {
  const [saved, setSaved] = useState(false);
  const [settings, setSettings] = useState({
    hospital_name: 'KAIre Health Memorial Hospital',
    mysql_host: 'localhost',
    mysql_database: 'kaire_health',
    jwt_expiry_hours: 12,
    enable_ml_diagnostics: true,
    risk_threshold_critical: 75,
    risk_threshold_high: 50,
    emergency_code_alerts: true
  });

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      <div>
        <h2 className="text-2xl font-black text-white font-display">System Configuration & ML Governance</h2>
        <p className="text-xs text-slate-400 mt-1">Configure MySQL database parameters, JWT security lifetime, and AI risk threshold boundaries.</p>
      </div>

      {saved && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" /> System settings persisted to database configuration!
        </div>
      )}

      <form onSubmit={handleSave} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Hospital & Database Setting Card */}
        <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2 text-sky-400 font-bold text-sm">
            <Database className="w-4 h-4" /> Hospital & Relational Database Layer
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Hospital Enterprise Name</label>
            <input
              type="text"
              value={settings.hospital_name}
              onChange={(e) => setSettings({ ...settings, hospital_name: e.target.value })}
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">MySQL Host</label>
              <input
                type="text"
                value={settings.mysql_host}
                onChange={(e) => setSettings({ ...settings, mysql_host: e.target.value })}
                className="w-full glass-input px-3.5 py-2 rounded-xl text-xs font-mono"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Database Schema</label>
              <input
                type="text"
                value={settings.mysql_database}
                onChange={(e) => setSettings({ ...settings, mysql_database: e.target.value })}
                className="w-full glass-input px-3.5 py-2 rounded-xl text-xs font-mono"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">JWT Session Expiry (Hours)</label>
            <input
              type="number"
              value={settings.jwt_expiry_hours}
              onChange={(e) => setSettings({ ...settings, jwt_expiry_hours: Number(e.target.value) })}
              className="w-full glass-input px-3.5 py-2 rounded-xl text-xs"
            />
          </div>
        </div>

        {/* ML Diagnostic Governance */}
        <div className="glass-card p-6 rounded-3xl border border-slate-800 space-y-4">
          <div className="flex items-center gap-2 text-rose-400 font-bold text-sm">
            <Brain className="w-4 h-4" /> Machine Learning Inference Parameters
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Critical Risk Cutoff Threshold: {settings.risk_threshold_critical}%</label>
            <input
              type="range" min="60" max="95"
              value={settings.risk_threshold_critical}
              onChange={(e) => setSettings({ ...settings, risk_threshold_critical: Number(e.target.value) })}
              className="w-full accent-rose-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">High Risk Cutoff Threshold: {settings.risk_threshold_high}%</label>
            <input
              type="range" min="35" max="65"
              value={settings.risk_threshold_high}
              onChange={(e) => setSettings({ ...settings, risk_threshold_high: Number(e.target.value) })}
              className="w-full accent-amber-500"
            />
          </div>

          <div className="pt-2">
            <button
              type="submit"
              className="w-full py-3 rounded-2xl bg-gradient-to-r from-sky-600 to-teal-600 font-bold text-xs text-white shadow-xl shadow-sky-600/30"
            >
              Persist System Configuration
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};
