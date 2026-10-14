import React, { useState } from 'react';
import { 
  Trophy, CheckCircle2, Award, ArrowUpRight, BarChart2, 
  Layers, ShieldCheck, GitCommit, FileText, Cpu, ChevronRight 
} from 'lucide-react';

const BENCHMARK_DATA = [
  {
    paradigm: 'Tier 1: Lexicon',
    model: 'Loughran-McDonald',
    accuracy: '56.18%',
    macroP: '44.01%',
    macroR: '43.54%',
    macroF1: '43.52%',
    weightedF1: '55.58%',
    badge: 'Lexicon Baseline',
    badgeColor: 'border-slate-700 text-slate-400 bg-slate-800/40',
    highlight: false
  },
  {
    paradigm: 'Tier 2: Classical ML',
    model: 'Multinomial Naive Bayes',
    accuracy: '74.71%',
    macroP: '80.40%',
    macroR: '52.60%',
    macroF1: '53.87%',
    weightedF1: '70.20%',
    badge: 'Classical TF-IDF',
    badgeColor: 'border-slate-700 text-slate-400 bg-slate-800/40',
    highlight: false
  },
  {
    paradigm: 'Tier 2: Classical ML',
    model: 'Logistic Regression',
    accuracy: '85.71%',
    macroP: '84.63%',
    macroR: '78.68%',
    macroF1: '81.23%',
    weightedF1: '85.38%',
    badge: 'Balanced Loss',
    badgeColor: 'border-slate-700 text-slate-400 bg-slate-800/40',
    highlight: false
  },
  {
    paradigm: 'Tier 2: Classical ML',
    model: 'Linear SVM',
    accuracy: '86.49%',
    macroP: '87.88%',
    macroR: '77.24%',
    macroF1: '81.29%',
    weightedF1: '85.91%',
    badge: 'Best Classical ML',
    badgeColor: 'border-indigo-500/30 text-indigo-300 bg-indigo-500/10',
    highlight: false
  },
  {
    paradigm: 'Tier 3: Transformer (ZS)',
    model: 'FinBERT Zero-Shot (HKUST)',
    accuracy: '88.42%',
    macroP: '89.11%',
    macroR: '84.22%',
    macroF1: '86.22%',
    weightedF1: '88.06%',
    badge: 'Zero-Shot Baseline',
    badgeColor: 'border-slate-700 text-slate-400 bg-slate-800/40',
    highlight: false
  },
  {
    paradigm: 'Tier 3: Transformer (FT)',
    model: 'FinBERT Fine-Tuned (Proposed)',
    accuracy: '92.08%',
    macroP: '88.97%',
    macroR: '90.69%',
    macroF1: '89.76%',
    weightedF1: '92.10%',
    badge: '🏆 SOTA Benchmark',
    badgeColor: 'border-emerald-500/50 text-emerald-300 bg-emerald-500/20 shadow-bullish-glow',
    highlight: true
  },
  {
    paradigm: 'Extension: Entity-Aware',
    model: 'Entity-FinBERT (SEntFiN 1.0)',
    accuracy: '84.09%',
    macroP: '84.31%',
    macroR: '83.94%',
    macroF1: '84.11%',
    weightedF1: '84.09%',
    badge: 'Entity Pair Disambiguation',
    badgeColor: 'border-cyan-500/40 text-cyan-300 bg-cyan-500/10',
    highlight: false
  }
];

const PIPELINE_STEPS = [
  {
    step: '01',
    title: 'Benchmark Data Ingestion',
    tech: 'FinancialPhraseBank & SEntFiN 1.0',
    desc: 'Stratified split (70/15/15) with zero sample overlap assertion to eliminate any risk of data leakage.'
  },
  {
    step: '02',
    title: 'Financial Normalizer',
    tech: 'cleaner.py (Deterministic Regex)',
    desc: 'Purges HTML entities & URLs while strictly preserving monetary symbols ($, €), percentage (%), and negation tokens.'
  },
  {
    step: '03',
    title: 'FinBERT Transformer',
    tech: '12-Layer, 768-dim Embeddings',
    desc: 'Domain-adapted BERT pretrained on financial corpora with 12 multi-head attention mechanisms.'
  },
  {
    step: '04',
    title: 'Class-Weighted Training',
    tech: 'CrossEntropyLoss(weight=w_c)',
    desc: 'Inverse frequency class weighting to combat ~60% neutral class imbalance and maximize Macro F1 score.'
  },
  {
    step: '05',
    title: 'FastAPI Microservice',
    tech: 'NVIDIA RTX 3050 AMP (FP16)',
    desc: 'Sub-20ms inference latency microservice with GPU warmup and Pydantic v2 schema validation.'
  },
  {
    step: '06',
    title: 'Cyber Dashboard',
    tech: 'React 19 + Recharts + Tailwind',
    desc: 'Real-time financial telemetry with live ticker news ingestion and statistical report rendering.'
  }
];

export default function BenchmarkShowcase() {
  const [selectedModel, setSelectedModel] = useState('FinBERT Fine-Tuned (Proposed)');

  return (
    <div className="space-y-8">
      {/* Top Banner: Scientific Excellence */}
      <div className="glass-panel rounded-2xl p-6 relative overflow-hidden border border-indigo-500/30">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                VERIFIED RIGOROUS SCIENTIFIC RESULTS
              </span>
              <span className="text-xs font-mono text-slate-400">IEEE 2-Column Standard</span>
            </div>
            <h2 className="text-xl font-extrabold text-white tracking-tight">
              Master Multi-Tier Comparative Benchmark Matrix
            </h2>
            <p className="text-xs text-slate-300 mt-1 max-w-3xl leading-relaxed">
              Empirical evaluation across Lexicon, Classical ML, and Pretrained Transformer paradigms on 518 frozen test samples of FinancialPhraseBank (75% agreement) and SEntFiN 1.0.
            </p>
          </div>

          {/* SOTA Badge */}
          <div className="bg-gradient-to-br from-indigo-900/40 to-slate-900/60 border border-indigo-500/40 rounded-xl p-4 flex items-center gap-4 shadow-cyber-sm shrink-0">
            <div className="h-12 w-12 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
              <Trophy className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Top Performance</span>
              <div className="text-lg font-bold font-mono text-white">92.08% Acc / 89.76% F1</div>
              <span className="text-[10px] text-emerald-400 font-mono">FinBERT Fine-Tuned (HKUST)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Benchmark Table */}
      <div className="glass-panel rounded-2xl overflow-hidden border border-slate-800">
        <div className="p-4 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-cyan-400" />
            <span className="text-xs font-mono font-bold text-slate-200 uppercase tracking-wider">
              Test Partition Performance (N = 518)
            </span>
          </div>
          <span className="text-[11px] font-mono text-slate-500 hidden sm:inline">
            Exported from reports/tables/benchmark_results.md
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="bg-slate-900/90 text-slate-400 border-b border-slate-800 text-[11px]">
                <th className="py-3 px-4">Paradigm</th>
                <th className="py-3 px-4">Model Candidate</th>
                <th className="py-3 px-3 text-right">Accuracy</th>
                <th className="py-3 px-3 text-right">Macro P</th>
                <th className="py-3 px-3 text-right">Macro R</th>
                <th className="py-3 px-3 text-right font-bold text-slate-200">Macro F1</th>
                <th className="py-3 px-3 text-right">Weighted F1</th>
                <th className="py-3 px-4 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {BENCHMARK_DATA.map((row, idx) => (
                <tr
                  key={idx}
                  className={`transition-colors ${
                    row.highlight
                      ? 'bg-emerald-950/20 hover:bg-emerald-950/30 text-white font-semibold'
                      : 'hover:bg-slate-800/30 text-slate-300'
                  }`}
                >
                  <td className="py-3.5 px-4 text-slate-400">{row.paradigm}</td>
                  <td className="py-3.5 px-4 font-bold flex items-center gap-2">
                    {row.highlight && <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>}
                    {row.model}
                  </td>
                  <td className="py-3.5 px-3 text-right">{row.accuracy}</td>
                  <td className="py-3.5 px-3 text-right text-slate-400">{row.macroP}</td>
                  <td className="py-3.5 px-3 text-right text-slate-400">{row.macroR}</td>
                  <td className={`py-3.5 px-3 text-right font-bold ${row.highlight ? 'text-emerald-400 text-sm' : 'text-slate-200'}`}>
                    {row.macroF1}
                  </td>
                  <td className="py-3.5 px-3 text-right text-slate-400">{row.weightedF1}</td>
                  <td className="py-3.5 px-4 text-center">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-mono border ${row.badgeColor}`}>
                      {row.badge}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* McNemar Statistical Hypothesis Testing Card */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 glass-panel rounded-2xl p-6 border border-cyan-500/30 space-y-4">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base font-bold text-white tracking-tight">
              Statistical Significance Verification (McNemar's Test)
            </h3>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            In accordance with rigorous computational linguistics methodology, model superiority must be validated by statistical testing. We performed pairwise **McNemar's Test with Edwards' Continuity Correction** between FinBERT Fine-Tuned and all baselines.
          </p>

          <div className="space-y-3 pt-2">
            {/* Comparison vs Linear SVM */}
            <div className="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-white">
                  FinBERT Fine-Tuned vs. Linear SVM (Best Tier 2 Baseline)
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                  p = 0.0021 &lt; 0.05
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2 text-[11px] font-mono text-slate-400">
                <div>Chi-Square (χ²): <strong className="text-slate-200">9.4458</strong></div>
                <div>Discordant (b / c): <strong className="text-slate-200">56 / 27</strong></div>
                <div>Confidence: <strong className="text-emerald-400">99.79%</strong></div>
              </div>
              <p className="text-[11px] text-slate-400 leading-tight">
                ★ <strong>Statistically Significant:</strong> FinBERT made 56 correct predictions on samples where SVM failed, compared to only 27 in reverse.
              </p>
            </div>

            {/* Comparison vs Lexicon */}
            <div className="p-3.5 bg-slate-900/80 rounded-xl border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-white">
                  FinBERT Fine-Tuned vs. Loughran-McDonald (Tier 1 Lexicon)
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                  p = 4.26e-35 &lt;&lt; 0.001
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2 text-[11px] font-mono text-slate-400">
                <div>Chi-Square (χ²): <strong className="text-slate-200">152.79</strong></div>
                <div>Discordant (b / c): <strong className="text-slate-200">205 / 19</strong></div>
                <div>Confidence: <strong className="text-emerald-400">&gt;99.99%</strong></div>
              </div>
            </div>
          </div>
        </div>

        {/* 2x2 Contingency Matrix Visualizer */}
        <div className="lg:col-span-5 glass-panel rounded-2xl p-6 border border-slate-800 flex flex-col justify-between space-y-4">
          <div>
            <span className="text-xs font-mono font-semibold tracking-wider text-slate-300 uppercase block mb-1">
              2x2 Contingency Matrix (FinBERT vs SVM)
            </span>
            <p className="text-[11px] text-slate-400">
              Distribution of paired sample test outcomes on N = 518.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-3 text-center font-mono">
            <div className="bg-slate-900/80 border border-emerald-500/30 rounded-xl p-3">
              <span className="text-[10px] text-slate-400 block">Both Correct</span>
              <span className="text-2xl font-bold text-emerald-400">421</span>
              <span className="text-[9px] text-slate-500 block">Agreement</span>
            </div>

            <div className="bg-slate-900/80 border border-indigo-500/40 rounded-xl p-3">
              <span className="text-[10px] text-indigo-300 block">FinBERT Won (b)</span>
              <span className="text-2xl font-bold text-indigo-400">56</span>
              <span className="text-[9px] text-slate-500 block">FinBERT ✓ / SVM ✗</span>
            </div>

            <div className="bg-slate-900/80 border border-rose-500/30 rounded-xl p-3">
              <span className="text-[10px] text-rose-300 block">SVM Won (c)</span>
              <span className="text-2xl font-bold text-rose-400">27</span>
              <span className="text-[9px] text-slate-500 block">SVM ✓ / FinBERT ✗</span>
            </div>

            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-3">
              <span className="text-[10px] text-slate-400 block">Both Failed</span>
              <span className="text-2xl font-bold text-slate-500">14</span>
              <span className="text-[9px] text-slate-500 block">Ambiguous Cases</span>
            </div>
          </div>

          <div className="text-[11px] font-mono text-slate-400 pt-2 border-t border-slate-800">
            Formula: <code className="text-cyan-300">χ² = (|b - c| - 1)² / (b + c) = 9.4458</code>
          </div>
        </div>
      </div>

      {/* End-to-End Pipeline Architecture */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-indigo-400" />
          <h3 className="text-base font-bold text-white tracking-tight">
            End-to-End Scientific Architecture & System Pipeline
          </h3>
        </div>
        <p className="text-xs text-slate-300">
          From raw multi-agreement financial text ingestion to GPU-accelerated low-latency REST inference.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5 pt-2">
          {PIPELINE_STEPS.map((step, idx) => (
            <div
              key={idx}
              className="p-4 bg-slate-900/60 border border-slate-800/80 rounded-xl space-y-2 hover:border-slate-700 transition-all"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-indigo-400">{step.step}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {step.tech}
                </span>
              </div>
              <h4 className="text-xs font-bold text-white">{step.title}</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">{step.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
