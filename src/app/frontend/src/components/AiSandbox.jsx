import React, { useState } from 'react';
import { 
  Zap, Sparkles, Send, CheckCircle2, AlertTriangle, HelpCircle, 
  Cpu, ArrowRight, CornerDownLeft, RefreshCw, Layers 
} from 'lucide-react';
import { predictSentiment } from '../services/api';

const PRESET_HEADLINES = [
  {
    category: 'Strong Bullish',
    badgeColor: 'border-emerald-500/30 text-emerald-400 bg-emerald-500/10',
    text: 'Operating profit surged by 45% to EUR 120 million, significantly exceeding analyst forecasts.'
  },
  {
    category: 'Severe Bearish',
    badgeColor: 'border-rose-500/30 text-rose-400 bg-rose-500/10',
    text: 'Net income plummeted by 38% amid widening operating losses and European supply chain disruptions.'
  },
  {
    category: 'Strict Neutral',
    badgeColor: 'border-slate-500/30 text-slate-400 bg-slate-500/10',
    text: 'The board of directors will publish the interim quarterly financial report on next Tuesday.'
  },
  {
    category: 'Financial Nuance (Loss Narrowed)',
    badgeColor: 'border-cyan-500/30 text-cyan-400 bg-cyan-500/10',
    text: "In the second quarter of 2024, the group's pretax loss narrowed to EUR 400,000 from EUR 600,000."
  }
];

export default function AiSandbox() {
  const [text, setText] = useState(PRESET_HEADLINES[0].text);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState({
    text: PRESET_HEADLINES[0].text,
    sentiment: 'positive',
    confidence: 0.9634,
    probabilities: { positive: 0.9634, neutral: 0.0311, negative: 0.0055 },
    latency: 18
  });

  const handleAnalyze = async () => {
    if (!text.trim() || loading) return;
    setLoading(true);
    try {
      const res = await predictSentiment(text.trim());
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      handleAnalyze();
    }
  };

  const sentimentStyles = {
    positive: {
      color: 'text-emerald-400',
      border: 'border-emerald-500/40',
      bg: 'bg-emerald-950/30',
      glow: 'shadow-bullish-glow',
      barColor: 'bg-emerald-500',
      label: 'POSITIVE / BULLISH'
    },
    negative: {
      color: 'text-rose-400',
      border: 'border-rose-500/40',
      bg: 'bg-rose-950/30',
      glow: 'shadow-bearish-glow',
      barColor: 'bg-rose-500',
      label: 'NEGATIVE / BEARISH'
    },
    neutral: {
      color: 'text-slate-300',
      border: 'border-slate-700/60',
      bg: 'bg-slate-900/40',
      glow: 'shadow-cyber-sm',
      barColor: 'bg-slate-400',
      label: 'NEUTRAL'
    }
  };

  const activeStyle = sentimentStyles[result?.sentiment] || sentimentStyles.neutral;

  return (
    <div className="space-y-6">
      {/* Intro Header */}
      <div className="glass-panel rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Zap className="w-5 h-5 text-indigo-400" />
              Interactive FinBERT Sentiment Sandbox & Explainability
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Enter any real-world financial headline, earnings call transcript, or regulatory statement to test 12-layer FinBERT inference.
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs font-mono bg-slate-900/60 px-3 py-1.5 rounded-lg border border-slate-800 self-start md:self-auto">
            <Cpu className="w-4 h-4 text-cyan-400" />
            <span>CUDA TENSOR CORES ACTIVE</span>
          </div>
        </div>
      </div>

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (Input & Presets): 7 cols */}
        <div className="lg:col-span-7 space-y-4">
          <div className="glass-panel rounded-2xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs font-mono font-semibold tracking-wider text-slate-300 uppercase">
                Input Financial Sentence
              </label>
              <span className="text-[11px] font-mono text-slate-500">
                {text.length} chars • Ctrl + Enter to run
              </span>
            </div>

            <div className="relative">
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={handleKeyDown}
                rows={4}
                placeholder="Enter financial sentence (e.g. Sales rose 15% to $120 million)..."
                className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none font-sans"
              />
            </div>

            <div className="flex items-center justify-between pt-1">
              <button
                type="button"
                onClick={() => setText('')}
                className="text-xs text-slate-500 hover:text-slate-300 font-mono transition-colors"
              >
                Clear input
              </button>

              <button
                type="button"
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
                className="btn-shimmer px-6 py-2.5 rounded-xl text-white text-xs font-bold tracking-wide uppercase shadow-cyber-sm flex items-center gap-2 disabled:opacity-50 transition-all cursor-pointer"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Evaluating Tensor...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-cyan-200" />
                    <span>Analyze with FinBERT</span>
                    <CornerDownLeft className="w-3.5 h-3.5 text-slate-200 opacity-60" />
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Quick Presets */}
          <div className="glass-panel rounded-2xl p-5 space-y-3">
            <span className="text-xs font-mono font-semibold tracking-wider text-slate-400 uppercase">
              Curated Financial Test Scenarios
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {PRESET_HEADLINES.map((preset, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setText(preset.text);
                  }}
                  className="p-3 text-left bg-slate-900/50 hover:bg-slate-800/60 border border-slate-800 hover:border-slate-700 rounded-xl transition-all group"
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${preset.badgeColor}`}>
                      {preset.category}
                    </span>
                    <ArrowRight className="w-3 h-3 text-slate-600 group-hover:text-cyan-400 transition-colors" />
                  </div>
                  <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed">
                    "{preset.text}"
                  </p>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column (Inference Result & Probability Bars): 5 cols */}
        <div className="lg:col-span-5 space-y-4">
          <div className={`glass-panel rounded-2xl p-6 border ${activeStyle.border} ${activeStyle.bg} ${activeStyle.glow} transition-all duration-300 space-y-6`}>
            {/* Top: Classification Badge */}
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                  Predicted Sentiment
                </span>
                <div className={`text-2xl font-extrabold font-mono mt-1 ${activeStyle.color} flex items-center gap-2`}>
                  {activeStyle.label}
                </div>
              </div>
              <div className="text-right">
                <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Confidence</span>
                <div className="text-2xl font-bold font-mono text-white mt-1">
                  {Math.round((result?.confidence || 0) * 1000) / 10}%
                </div>
              </div>
            </div>

            {/* Latency & Device metadata */}
            <div className="flex items-center justify-between py-2.5 px-3.5 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs font-mono">
              <span className="text-slate-400">Inference Latency:</span>
              <span className="text-emerald-400 font-bold">{result?.latency || 18} ms</span>
            </div>

            {/* Probability Bars (Softmax outputs) */}
            <div className="space-y-3.5 pt-2 border-t border-slate-800/80">
              <span className="text-xs font-mono font-semibold tracking-wider text-slate-300 uppercase block">
                Softmax Probability Distribution
              </span>

              {/* Positive Bar */}
              <div>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-emerald-400 flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                    Positive (Bullish)
                  </span>
                  <span className="text-slate-200 font-bold">
                    {Math.round((result?.probabilities?.positive || 0) * 1000) / 10}%
                  </span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div
                    style={{ width: `${(result?.probabilities?.positive || 0) * 100}%` }}
                    className="h-full bg-emerald-500 transition-all duration-500 ease-out"
                  />
                </div>
              </div>

              {/* Neutral Bar */}
              <div>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-slate-300 flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-slate-400"></span>
                    Neutral (Factual)
                  </span>
                  <span className="text-slate-200 font-bold">
                    {Math.round((result?.probabilities?.neutral || 0) * 1000) / 10}%
                  </span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div
                    style={{ width: `${(result?.probabilities?.neutral || 0) * 100}%` }}
                    className="h-full bg-slate-400 transition-all duration-500 ease-out"
                  />
                </div>
              </div>

              {/* Negative Bar */}
              <div>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-rose-400 flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                    Negative (Bearish)
                  </span>
                  <span className="text-slate-200 font-bold">
                    {Math.round((result?.probabilities?.negative || 0) * 1000) / 10}%
                  </span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div
                    style={{ width: `${(result?.probabilities?.negative || 0) * 100}%` }}
                    className="h-full bg-rose-500 transition-all duration-500 ease-out"
                  />
                </div>
              </div>
            </div>

            {/* Architecture Details Footer */}
            <div className="pt-4 border-t border-slate-800/80 text-[11px] font-mono text-slate-400 space-y-1">
              <div className="flex justify-between">
                <span>Architecture:</span>
                <span className="text-slate-200 font-semibold">12-layer Transformer (BERT-base)</span>
              </div>
              <div className="flex justify-between">
                <span>Max Sequence Length:</span>
                <span className="text-slate-200">128 tokens</span>
              </div>
              <div className="flex justify-between">
                <span>Attention Heads:</span>
                <span className="text-slate-200">12 Multi-Head Attention</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
