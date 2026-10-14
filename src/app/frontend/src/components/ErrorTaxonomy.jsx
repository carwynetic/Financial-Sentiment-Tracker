import React, { useState } from 'react';
import { 
  AlertOctagon, CheckCircle2, ChevronDown, ChevronRight, 
  HelpCircle, Info, Sparkles, Filter 
} from 'lucide-react';

const ERROR_DISTRIBUTION = [
  { mode: 'Neutral -> Positive', count: 13, pct: '31.7%', severity: 'Low Risk', color: 'text-amber-400' },
  { mode: 'Positive -> Neutral', count: 12, pct: '29.3%', severity: 'Low Risk', color: 'text-amber-400' },
  { mode: 'Positive -> Negative', count: 8, pct: '19.5%', severity: 'Critical Reversal', color: 'text-rose-400' },
  { mode: 'Negative -> Positive', count: 4, pct: '9.8%', severity: 'Critical Reversal', color: 'text-rose-400' },
  { mode: 'Neutral -> Negative', count: 3, pct: '7.3%', severity: 'Minor Bias', color: 'text-slate-400' },
  { mode: 'Negative -> Neutral', count: 1, pct: '2.4%', severity: 'Minor Bias', color: 'text-slate-400' }
];

const TAXONOMY_CASES = [
  {
    mode: 'Positive -> Negative',
    badge: 'Contrastive Clauses & Loss Reduction',
    sentence: "In the second quarter of 2010 , the group 's pretax loss narrowed to EUR 400,000 from EUR 600,000 .",
    groundTruth: 'Positive',
    finbertPred: 'Negative',
    explanation:
      "Financial Nuance Trap: The token 'loss' possesses strong negative valence in general language models. While a narrowing loss reflects operational improvement (Positive), BERT self-attention over-indexes on lexical negativity without multi-clause financial accounting knowledge."
  },
  {
    mode: 'Positive -> Negative',
    badge: 'Turnaround & Swung to Profit',
    sentence: "Finnish wood products technology supplier Raute Oyj said today it swung to a net profit of EUR3m for the first nine months versus a net loss of EUR5.2m a year earlier .",
    groundTruth: 'Positive',
    finbertPred: 'Negative',
    explanation:
      "Temporal Relativity Trap: The sentence describes a dramatic positive turnaround ('swung to profit'), but contains both 'profit' and 'loss'. When 'loss' appears near numerical amounts, baseline representations can misjudge polarity."
  },
  {
    mode: 'Negative -> Positive',
    badge: 'Deceptive Leadership Noun',
    sentence: "Coca-Cola was the market leader of manufacturers with a market share of 36.9 % , down 2.2 % from the corresponding period in 2004-2005 .",
    groundTruth: 'Negative',
    finbertPred: 'Positive',
    explanation:
      "Halo Effect Trap: Strong positive branding words like 'market leader' overpower the subtle numeric decline signal ('down 2.2%'). The model prioritizes entity prestige over statistical erosion."
  },
  {
    mode: 'Neutral -> Positive',
    badge: 'Growth Without Margin Context',
    sentence: "Following the issue , the number of shares in the Swedish company will grow by 9 % .",
    groundTruth: 'Neutral',
    finbertPred: 'Positive',
    explanation:
      "Dilution Trap: 'Grow by 9%' triggers positive lexical polarity, but in corporate finance, increasing share count indicates dilution of existing shareholder value, which is neutral or potentially negative."
  },
  {
    mode: 'Neutral -> Negative',
    badge: 'Corporate Jargon & Reorganization',
    sentence: "As a consequence the Works Council had withdrawn its petition to suspend the reorganisation .",
    groundTruth: 'Neutral',
    finbertPred: 'Negative',
    explanation:
      "Conflict Terminology: Legal and industrial relation terms like 'petition' and 'suspend' carry heavy negative friction connotations in common parlance, whereas legally this was a neutral procedural settlement."
  }
];

export default function ErrorTaxonomy() {
  const [selectedFilter, setSelectedFilter] = useState('ALL');

  const filteredCases = selectedFilter === 'ALL'
    ? TAXONOMY_CASES
    : TAXONOMY_CASES.filter((c) => c.mode === selectedFilter);

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-bold flex items-center gap-1">
                <AlertOctagon className="w-3.5 h-3.5" />
                TASK 4.3 EMPIRICAL AUDIT
              </span>
              <span className="text-xs font-mono text-slate-400">Total N = 518</span>
            </div>
            <h2 className="text-lg font-bold text-white tracking-tight">
              Qualitative Failure Mode Analysis & Error Taxonomy
            </h2>
            <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
              Transparent scientific examination of the 41 misclassified test samples (7.92% total error rate). We identify 3 fundamental financial failure modes: Temporal relativity, halo effect, and share dilution.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-slate-900/80 p-3.5 rounded-xl border border-slate-800 shrink-0 font-mono text-xs">
            <div>
              <span className="text-slate-400 text-[10px] uppercase block">Global Accuracy</span>
              <span className="text-emerald-400 font-bold text-lg">92.08%</span>
            </div>
            <div className="h-8 w-px bg-slate-800" />
            <div>
              <span className="text-slate-400 text-[10px] uppercase block">Error Count</span>
              <span className="text-rose-400 font-bold text-lg">41 / 518</span>
            </div>
          </div>
        </div>
      </div>

      {/* Breakdown Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Distribution Table (5 cols) */}
        <div className="lg:col-span-5 glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-semibold tracking-wider text-slate-300 uppercase">
              Confusion Distribution
            </span>
            <span className="text-[10px] font-mono text-slate-500">6 Error Modes</span>
          </div>

          <div className="space-y-2">
            {ERROR_DISTRIBUTION.map((item, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedFilter(selectedFilter === item.mode ? 'ALL' : item.mode)}
                className={`w-full p-2.5 rounded-xl text-left font-mono text-xs transition-all flex items-center justify-between border ${
                  selectedFilter === item.mode
                    ? 'bg-slate-800/90 border-cyan-500/50 shadow-cyber-sm'
                    : 'bg-slate-900/60 hover:bg-slate-800/50 border-slate-800'
                }`}
              >
                <div>
                  <span className="text-slate-200 font-semibold block">{item.mode}</span>
                  <span className={`text-[10px] ${item.color}`}>{item.severity}</span>
                </div>
                <div className="text-right">
                  <span className="text-white font-bold block">{item.count} cases</span>
                  <span className="text-[10px] text-slate-400">{item.pct}</span>
                </div>
              </button>
            ))}
          </div>

          {selectedFilter !== 'ALL' && (
            <button
              onClick={() => setSelectedFilter('ALL')}
              className="w-full py-1.5 text-center text-xs font-mono text-cyan-400 hover:text-cyan-300 border border-slate-700/60 rounded-lg bg-slate-900/40"
            >
              Reset Filter (Show All)
            </button>
          )}
        </div>

        {/* Right Column: Case Inspections (7 cols) */}
        <div className="lg:col-span-7 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-semibold tracking-wider text-slate-300 uppercase">
              Failure Mode Deep Dives ({filteredCases.length})
            </span>
            <span className="text-[11px] font-mono text-slate-500">
              Annotated from reports/tables/error_taxonomy.md
            </span>
          </div>

          <div className="space-y-3">
            {filteredCases.map((item, idx) => (
              <div
                key={idx}
                className="glass-panel rounded-xl p-4 border border-slate-800 hover:border-slate-700 transition-all space-y-2.5"
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
                    {item.badge}
                  </span>
                  <div className="flex items-center gap-2 text-xs font-mono">
                    <span className="text-slate-400">Ground Truth: <strong className="text-emerald-400">{item.groundTruth}</strong></span>
                    <span className="text-slate-600">→</span>
                    <span className="text-slate-400">Predicted: <strong className="text-rose-400">{item.finbertPred}</strong></span>
                  </div>
                </div>

                <p className="text-xs text-slate-200 font-sans italic bg-slate-900/80 p-3 rounded-lg border border-slate-800/80 leading-relaxed">
                  "{item.sentence}"
                </p>

                <div className="text-[11px] text-slate-400 flex items-start gap-2 bg-slate-950/40 p-2.5 rounded-lg border border-slate-800/60">
                  <Info className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                  <p className="leading-relaxed">{item.explanation}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
