import React from 'react';

export const StatCard = ({ title, value, subtitle, icon: Icon, color = 'sky', trend, onClick }) => {
  const colorMap = {
    sky: 'from-sky-500/20 to-sky-600/5 text-sky-400 border-sky-500/20',
    teal: 'from-teal-500/20 to-teal-600/5 text-teal-400 border-teal-500/20',
    rose: 'from-rose-500/20 to-rose-600/5 text-rose-400 border-rose-500/20',
    amber: 'from-amber-500/20 to-amber-600/5 text-amber-400 border-amber-500/20',
    indigo: 'from-indigo-500/20 to-indigo-600/5 text-indigo-400 border-indigo-500/20',
    emerald: 'from-emerald-500/20 to-emerald-600/5 text-emerald-400 border-emerald-500/20',
  };

  const selectedColor = colorMap[color] || colorMap.sky;

  return (
    <div 
      onClick={onClick}
      className={`glass-card p-5 rounded-2xl border transition-all duration-300 relative overflow-hidden group ${onClick ? 'cursor-pointer hover:scale-[1.02]' : ''}`}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">{title}</p>
          <h3 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">{value}</h3>
          {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
          {trend && (
            <div className="flex items-center gap-1 mt-2">
              <span className={`text-xs font-medium ${trend.positive ? 'text-emerald-400' : 'text-rose-400'}`}>
                {trend.positive ? '↑' : '↓'} {trend.value}
              </span>
              <span className="text-[11px] text-slate-400">vs last week</span>
            </div>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-xl bg-gradient-to-br border ${selectedColor} group-hover:scale-110 transition-transform duration-300`}>
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
      <div className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r ${selectedColor} opacity-50`} />
    </div>
  );
};

export const Badge = ({ children, variant = 'default', size = 'sm' }) => {
  const variantMap = {
    default: 'bg-slate-700/60 text-slate-200 border-slate-600',
    success: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    warning: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    danger: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
    info: 'bg-sky-500/10 text-sky-400 border-sky-500/30',
    critical: 'bg-rose-600/20 text-rose-300 border-rose-500/50 animate-pulse font-bold',
    purple: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
  };

  const sizeMap = {
    xs: 'px-2 py-0.5 text-[10px]',
    sm: 'px-2.5 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm'
  };

  return (
    <span className={`inline-flex items-center gap-1 font-medium rounded-full border ${variantMap[variant] || variantMap.default} ${sizeMap[size]}`}>
      {children}
    </span>
  );
};

export const LoadingSpinner = ({ label = 'Loading clinical data...' }) => (
  <div className="flex flex-col items-center justify-center p-12 gap-3">
    <div className="w-10 h-10 border-3 border-sky-500/20 border-t-sky-400 rounded-full animate-spin" />
    <p className="text-xs text-slate-400 font-medium tracking-wide animate-pulse">{label}</p>
  </div>
);

export const Modal = ({ isOpen, onClose, title, children, maxWidth = 'max-w-2xl' }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div className={`glass-card w-full ${maxWidth} rounded-2xl border border-slate-700/70 overflow-hidden shadow-2xl animate-scaleUp`}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/60">
          <h3 className="text-lg font-bold text-white tracking-tight">{title}</h3>
          <button 
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          >
            ✕
          </button>
        </div>
        <div className="p-6 max-h-[80vh] overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
};
