import React from 'react';
import { ShieldCheck, Heart, Terminal, BookOpen, ExternalLink } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-800/80 bg-obsidian-950 py-8 text-xs font-mono text-slate-500">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded-lg bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400">
              <Terminal className="w-3.5 h-3.5" />
            </div>
            <span className="text-slate-300 font-bold">FINBERT FINANCIAL SENTIMENT TRACKER</span>
            <span className="text-slate-600">•</span>
            <span className="text-slate-400">TMG301 Text Mining • FPT University</span>
          </div>

          <div className="flex items-center gap-4 text-slate-400">
            <span className="flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>Zero-Leakage Stratified Split</span>
            </span>
            <span className="text-slate-600">•</span>
            <span>McNemar Verified (p = 0.0021)</span>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between gap-2 pt-4 border-t border-slate-900 text-[11px] text-slate-500">
          <p>
            Powered by FinBERT-Tone (110M) • PyTorch Mixed Precision • FastAPI Microservice • React & Tailwind
          </p>
          <p>
            Designed for Bloomberg Terminal 2.0 & Cyber FinTech UX
          </p>
        </div>
      </div>
    </footer>
  );
}
