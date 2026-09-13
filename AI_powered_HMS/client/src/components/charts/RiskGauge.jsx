import React from 'react';

export const RiskGauge = ({ score = 0, level = 'Low', confidence = 89, disease = 'Heart Disease', size }) => {
  const getMeterColor = (val) => {
    if (val >= 75) return 'from-rose-600 via-rose-500 to-amber-500 text-rose-400';
    if (val >= 50) return 'from-amber-600 via-amber-500 to-yellow-500 text-amber-400';
    if (val >= 25) return 'from-sky-600 via-teal-500 to-emerald-500 text-sky-400';
    return 'from-emerald-600 via-teal-500 to-sky-500 text-emerald-400';
  };

  const getRiskLabel = (val) => {
    if (level && level !== 'Low') return level;
    if (val >= 75) return 'High';
    if (val >= 45) return 'Moderate';
    return 'Low';
  };

  const computedLevel = getRiskLabel(score);

  return (
    <div className="glass-card p-6 rounded-3xl border border-slate-800 flex flex-col items-center justify-center text-center relative overflow-hidden">
      {confidence > 0 && (
        <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full text-[10px] font-extrabold bg-slate-800 text-slate-300 border border-slate-700">
          Confidence: {confidence}%
        </div>
      )}

      <p className="text-xs uppercase font-extrabold text-slate-400 tracking-wider mb-2">AI Risk Stratification</p>
      <h3 className="text-lg font-black text-white">{disease}</h3>

      {/* Circular Progress Gauge */}
      <div className="relative w-40 h-40 my-4 flex items-center justify-center">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
          <path
            className="text-slate-800"
            strokeWidth="3.5"
            stroke="currentColor"
            fill="none"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <path
            className={`stroke-current transition-all duration-1000 ${score >= 70 ? 'text-rose-500' : (score >= 45 ? 'text-amber-400' : 'text-emerald-400')}`}
            strokeDasharray={`${score}, 100`}
            strokeLinecap="round"
            strokeWidth="3.8"
            fill="none"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
          />
        </svg>

        <div className="absolute flex flex-col items-center">
          <span className="text-3xl font-black text-white tracking-tight">{score}%</span>
          <span className={`text-xs font-black uppercase tracking-wider ${score >= 70 ? 'text-rose-400' : (score >= 45 ? 'text-amber-400' : 'text-emerald-400')}`}>
            {computedLevel} Risk
          </span>
        </div>
      </div>

      <div className="w-full bg-slate-900/80 p-3 rounded-2xl border border-slate-800/80 mt-1 text-xs text-slate-300">
        Clinical Risk Model Inference Output
      </div>
    </div>
  );
};
