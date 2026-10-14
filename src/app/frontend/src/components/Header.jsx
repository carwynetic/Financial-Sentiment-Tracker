import React, { useState, useEffect } from 'react';
import { Activity, Cpu, Zap, Radio, Clock, ShieldCheck, Terminal, Layers } from 'lucide-react';

export default function Header({ activeTab, setActiveTab, health }) {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatUtc = (d) => {
    return d.toISOString().slice(11, 19) + ' UTC';
  };

  const formatLocal = (d) => {
    return d.toLocaleTimeString('en-GB');
  };

  const navItems = [
    { id: 'pulse', label: 'MARKET PULSE', icon: Activity, badge: 'LIVE' },
    { id: 'sandbox', label: 'AI SANDBOX', icon: Terminal, badge: 'INTERACTIVE' },
    { id: 'benchmark', label: 'SCIENTIFIC BENCHMARK', icon: ShieldCheck, badge: 'IEEE SOTA' },
    { id: 'taxonomy', label: 'ERROR TAXONOMY', icon: Layers, badge: '518 AUDIT' }
  ];

  return (
    <header className="border-b border-slate-800/80 bg-obsidian-900/90 backdrop-blur-xl sticky top-0 z-50">
      {/* Top Telemetry Strip */}
      <div className="border-b border-slate-800/50 px-4 py-1.5 flex flex-wrap items-center justify-between text-[11px] font-mono text-slate-400">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${health.online ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
              <span className={`relative inline-flex rounded-full h-2 w-2 ${health.online ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
            </span>
            <span className="text-slate-200 font-semibold tracking-wide">
              {health.online ? 'FASTAPI CORE: ONLINE' : 'STANDALONE RUNTIME: READY'}
            </span>
            <span className="text-slate-500">|</span>
            <span className="text-emerald-400 font-semibold">
              {health.latency ? `${health.latency}ms` : '<20ms'}
            </span>
          </div>

          <div className="hidden md:flex items-center gap-2 text-slate-400">
            <Cpu className="w-3.5 h-3.5 text-cyan-400" />
            <span>ACCELERATOR: <strong className="text-slate-200">NVIDIA RTX 3050 (AMP FP16)</strong></span>
          </div>

          <div className="hidden lg:flex items-center gap-2 text-slate-400">
            <Radio className="w-3.5 h-3.5 text-indigo-400" />
            <span>MODEL: <strong className="text-slate-200">FinBERT-Tone (110M Params)</strong></span>
          </div>
        </div>

        <div className="flex items-center gap-4 text-slate-400">
          <span className="hidden sm:inline px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-[10px]">
            TMG301 SCIENTIFIC PIPELINE
          </span>
          <div className="flex items-center gap-2">
            <Clock className="w-3.5 h-3.5 text-slate-500" />
            <span className="text-slate-300 font-semibold">{formatLocal(time)}</span>
            <span className="text-slate-500 text-[10px]">({formatUtc(time)})</span>
          </div>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Logo & Course Info */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-500 via-cyan-500 to-emerald-500 p-0.5 shadow-cyber-sm">
            <div className="h-full w-full bg-obsidian-900 rounded-[10px] flex items-center justify-center">
              <Activity className="w-5 h-5 text-emerald-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
                FinBERT <span className="text-xs px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono">TERMINAL 2.0</span>
              </h1>
            </div>
            <p className="text-xs text-slate-400">
              Financial Sentiment Tracker • <span className="text-slate-300">FPT University AI</span>
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0 scrollbar-none">
          {navItems.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`relative flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-medium transition-all duration-200 whitespace-nowrap ${
                  isActive
                    ? 'bg-slate-800/90 text-white border border-slate-700 shadow-cyber-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40 border border-transparent'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-cyan-400' : 'text-slate-500'}`} />
                <span>{tab.label}</span>
                {tab.badge && (
                  <span
                    className={`text-[9px] px-1.5 py-0.2 rounded font-mono ${
                      isActive
                        ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                        : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {tab.badge}
                  </span>
                )}
                {isActive && (
                  <span className="absolute bottom-0 left-2 right-2 h-0.5 bg-gradient-to-r from-indigo-500 to-cyan-400 rounded-full" />
                )}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
