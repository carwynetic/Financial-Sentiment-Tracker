import React, { useState } from 'react';
import { 
  Zap, Sparkles, Send, CheckCircle2, AlertTriangle, HelpCircle, 
  Cpu, ArrowRight, CornerDownLeft, RefreshCw, Layers, Target, Split, ShieldCheck
} from 'lucide-react';
import { predictSentiment, predictEntitySentiment } from '../services/api';

const PRESET_SENTENCE_HEADLINES = [
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
    category: 'Turnaround Nuance',
    badgeColor: 'border-cyan-500/30 text-cyan-400 bg-cyan-500/10',
    text: "In the second quarter of 2024, the group's pretax loss narrowed to EUR 400,000 from EUR 600,000."
  }
];

const PRESET_ENTITY_HEADLINES = [
  {
    title: 'Opposing Commodities & Currencies (Gold vs Rupee)',
    headline: 'Gold extends gains on festive buying, weak rupee',
    entities: ['Gold', 'rupee'],
    notes: 'Gold rises (+) while rupee weakens (-). Standard sentence models fail on this conflict.'
  },
  {
    title: 'Tech Semiconductor Polarization (Nvidia vs Intel)',
    headline: 'Nvidia surges on accelerating AI hyperscaler demand while Intel slashes foundry guidance',
    entities: ['Nvidia', 'Intel'],
    notes: 'Opposing corporate fortunes within the same semiconductor supply chain headline.'
  },
  {
    title: 'EV Market Rating Divergence (Tesla vs Ford)',
    headline: 'Barclays raises price target on Tesla but downgrades Ford on EV pricing competition',
    entities: ['Tesla', 'Ford'],
    notes: 'Upgrade vs Downgrade polarity in a single Wall Street analyst research note.'
  }
];

export default function AiSandbox() {
  const [mode, setMode] = useState('entity'); // 'sentence' | 'entity'
  
  // Sentence Mode State
  const [sentenceText, setSentenceText] = useState(PRESET_SENTENCE_HEADLINES[0].text);
  const [sentenceLoading, setSentenceLoading] = useState(false);
  const [sentenceResult, setSentenceResult] = useState({
    text: PRESET_SENTENCE_HEADLINES[0].text,
    sentiment: 'positive',
    confidence: 0.9634,
    probabilities: { positive: 0.9634, neutral: 0.0311, negative: 0.0055 },
    latency: 18
  });

  // Entity Mode State
  const [entityName, setEntityName] = useState('Gold');
  const [entityHeadline, setEntityHeadline] = useState('Gold extends gains on festive buying, weak rupee');
  const [entityLoading, setEntityLoading] = useState(false);
  const [entityResult, setEntityResult] = useState({
    entity: 'Gold',
    headline: 'Gold extends gains on festive buying, weak rupee',
    sentiment: 'positive',
    confidence: 0.9551,
    probabilities: { positive: 0.9551, neutral: 0.0363, negative: 0.0086 },
    latency: 19
  });

  const handleSentenceAnalyze = async () => {
    if (!sentenceText.trim() || sentenceLoading) return;
    setSentenceLoading(true);
    try {
      const res = await predictSentiment(sentenceText.trim());
      setSentenceResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setSentenceLoading(false);
    }
  };

  const handleEntityAnalyze = async (overrideEntity, overrideHeadline) => {
    const e = (overrideEntity !== undefined ? overrideEntity : entityName).trim();
    const h = (overrideHeadline !== undefined ? overrideHeadline : entityHeadline).trim();
    if (!e || !h || entityLoading) return;
    setEntityLoading(true);
    try {
      const res = await predictEntitySentiment(e, h);
      setEntityResult(res);
      if (overrideEntity !== undefined) setEntityName(overrideEntity);
      if (overrideHeadline !== undefined) setEntityHeadline(overrideHeadline);
    } catch (err) {
      console.error(err);
    } finally {
      setEntityLoading(false);
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

  const currentResult = mode === 'entity' ? entityResult : sentenceResult;
  const currentLoading = mode === 'entity' ? entityLoading : sentenceLoading;
  const activeStyle = sentimentStyles[currentResult?.sentiment] || sentimentStyles.neutral;

  return (
    <div className="space-y-6">
      {/* Intro Header & Mode Switcher */}
      <div className="glass-panel rounded-2xl p-6 relative overflow-hidden">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Zap className="w-5 h-5 text-indigo-400" />
              <h2 className="text-lg font-bold text-white">
                FinBERT Inference & Explainability Sandbox
              </h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Phase 3 & 4 Ready
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Switch between sentence-level classification and Sentence-Pair Cross-Attention for resolving multi-entity financial conflict.
            </p>
          </div>

          {/* Mode Switch Tabs */}
          <div className="flex items-center p-1 bg-slate-900/90 rounded-xl border border-slate-800 self-start lg:self-auto">
            <button
              type="button"
              onClick={() => setMode('entity')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                mode === 'entity'
                  ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Target className="w-3.5 h-3.5" />
              <span>Entity-Aware (SEntFiN 1.0)</span>
            </button>
            <button
              type="button"
              onClick={() => setMode('sentence')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                mode === 'sentence'
                  ? 'bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>Sentence-Level (PhraseBank)</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (Input & Controls): 7 cols */}
        <div className="lg:col-span-7 space-y-4">
          {mode === 'entity' ? (
            /* ================= ENTITY-AWARE MODE ================= */
            <div className="space-y-4">
              <div className="glass-panel rounded-2xl p-5 space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-mono font-semibold tracking-wider text-cyan-300 uppercase flex items-center gap-1.5">
                    <Target className="w-4 h-4 text-cyan-400" />
                    Target Entity / Asset / Ticker
                  </label>
                  <span className="text-[11px] font-mono text-slate-500">
                    Segment A Token [CLS] Entity [SEP]
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="sm:col-span-1">
                    <input
                      type="text"
                      value={entityName}
                      onChange={(e) => setEntityName(e.target.value)}
                      placeholder="e.g. Gold, TSLA, rupee"
                      className="w-full bg-slate-900/90 border border-cyan-500/40 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-cyan-300 placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition-all font-mono"
                    />
                  </div>
                  <div className="sm:col-span-2 flex items-center text-xs text-slate-400 bg-slate-900/50 px-3 py-2 rounded-xl border border-slate-800">
                    <Split className="w-4 h-4 text-cyan-400 mr-2 shrink-0" />
                    <span>Cross-attention maps this target directly to its contextual sentiment modifiers.</span>
                  </div>
                </div>

                <div className="space-y-1.5 pt-2">
                  <label className="text-xs font-mono font-semibold tracking-wider text-slate-300 uppercase">
                    Financial Headline / News Context
                  </label>
                  <textarea
                    value={entityHeadline}
                    onChange={(e) => setEntityHeadline(e.target.value)}
                    rows={3}
                    placeholder="Enter headline containing one or more entities..."
                    className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl p-3.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition-all resize-none font-sans"
                  />
                </div>

                {/* Token Pair Architecture Preview */}
                <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800/80 space-y-1.5 font-mono text-[11px]">
                  <div className="text-slate-400 flex items-center gap-1.5">
                    <Cpu className="w-3.5 h-3.5 text-indigo-400" />
                    <span>Cross-Attention Input Encoding (Segment 0 & 1):</span>
                  </div>
                  <div className="text-slate-200 overflow-x-auto whitespace-nowrap py-1">
                    <span className="text-indigo-400 font-bold">[CLS]</span>{' '}
                    <span className="text-cyan-300 bg-cyan-950/40 px-1.5 py-0.5 rounded border border-cyan-500/30 font-semibold">{entityName || '<Target>'}</span>{' '}
                    <span className="text-indigo-400 font-bold">[SEP]</span>{' '}
                    <span className="text-slate-300">{entityHeadline || '<Headline>'}</span>{' '}
                    <span className="text-indigo-400 font-bold">[SEP]</span>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <button
                    type="button"
                    onClick={() => { setEntityName(''); setEntityHeadline(''); }}
                    className="text-xs text-slate-500 hover:text-slate-300 font-mono transition-colors"
                  >
                    Clear inputs
                  </button>

                  <button
                    type="button"
                    onClick={() => handleEntityAnalyze()}
                    disabled={entityLoading || !entityName.trim() || !entityHeadline.trim()}
                    className="btn-shimmer px-6 py-2.5 rounded-xl text-white text-xs font-bold tracking-wide uppercase shadow-cyber-sm flex items-center gap-2 disabled:opacity-50 transition-all cursor-pointer"
                  >
                    {entityLoading ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span>Evaluating Cross-Attention...</span>
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4 text-cyan-200" />
                        <span>Disambiguate Entity</span>
                        <CornerDownLeft className="w-3.5 h-3.5 text-slate-200 opacity-60" />
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Entity Preset Scenarios */}
              <div className="glass-panel rounded-2xl p-5 space-y-3">
                <span className="text-xs font-mono font-semibold tracking-wider text-slate-400 uppercase">
                  Multi-Entity Conflict Presets (Click Entity to Test)
                </span>
                <div className="space-y-3">
                  {PRESET_ENTITY_HEADLINES.map((preset, idx) => (
                    <div
                      key={idx}
                      className="p-3.5 bg-slate-900/50 border border-slate-800 rounded-xl space-y-2 hover:border-slate-700 transition-all"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-semibold text-slate-200 font-sans">{preset.title}</span>
                        <div className="flex items-center gap-1.5">
                          {preset.entities.map((ent) => (
                            <button
                              key={ent}
                              type="button"
                              onClick={() => handleEntityAnalyze(ent, preset.headline)}
                              className={`text-[11px] font-mono font-bold px-2.5 py-1 rounded-md transition-all ${
                                entityName === ent && entityHeadline === preset.headline
                                  ? 'bg-cyan-500 text-slate-950 shadow-sm'
                                  : 'bg-slate-800 text-cyan-300 hover:bg-slate-700'
                              }`}
                            >
                              Test: {ent}
                            </button>
                          ))}
                        </div>
                      </div>
                      <p className="text-xs text-slate-300 italic">"{preset.headline}"</p>
                      <p className="text-[11px] text-slate-500 font-mono">{preset.notes}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            /* ================= SENTENCE LEVEL MODE ================= */
            <div className="space-y-4">
              <div className="glass-panel rounded-2xl p-5 space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-mono font-semibold tracking-wider text-slate-300 uppercase">
                    Input Financial Sentence (Financial PhraseBank Format)
                  </label>
                  <span className="text-[11px] font-mono text-slate-500">
                    {sentenceText.length} chars • Ctrl + Enter to run
                  </span>
                </div>

                <div className="relative">
                  <textarea
                    value={sentenceText}
                    onChange={(e) => setSentenceText(e.target.value)}
                    rows={4}
                    placeholder="Enter financial sentence (e.g. Sales rose 15% to $120 million)..."
                    className="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none font-sans"
                  />
                </div>

                <div className="flex items-center justify-between pt-1">
                  <button
                    type="button"
                    onClick={() => setSentenceText('')}
                    className="text-xs text-slate-500 hover:text-slate-300 font-mono transition-colors"
                  >
                    Clear input
                  </button>

                  <button
                    type="button"
                    onClick={handleSentenceAnalyze}
                    disabled={sentenceLoading || !sentenceText.trim()}
                    className="btn-shimmer px-6 py-2.5 rounded-xl text-white text-xs font-bold tracking-wide uppercase shadow-cyber-sm flex items-center gap-2 disabled:opacity-50 transition-all cursor-pointer"
                  >
                    {sentenceLoading ? (
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

              {/* Quick Sentence Presets */}
              <div className="glass-panel rounded-2xl p-5 space-y-3">
                <span className="text-xs font-mono font-semibold tracking-wider text-slate-400 uppercase">
                  Curated Financial Test Scenarios
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {PRESET_SENTENCE_HEADLINES.map((preset, idx) => (
                    <button
                      key={idx}
                      onClick={() => setSentenceText(preset.text)}
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
          )}
        </div>

        {/* Right Column (Inference Result & Probability Bars): 5 cols */}
        <div className="lg:col-span-5 space-y-4">
          <div className={`glass-panel rounded-2xl p-6 border ${activeStyle.border} ${activeStyle.bg} ${activeStyle.glow} transition-all duration-300 space-y-6`}>
            {/* Top: Classification Badge */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">
                  {mode === 'entity' ? (
                    <span className="text-cyan-300 font-semibold flex items-center gap-1">
                      <Target className="w-3.5 h-3.5" /> Target: {currentResult?.entity || entityName}
                    </span>
                  ) : (
                    'Sentence Sentiment'
                  )}
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900/80 text-slate-400 border border-slate-800">
                  {mode === 'entity' ? 'Cross-Attention Model' : 'PhraseBank Model'}
                </span>
              </div>

              <div className="flex items-start justify-between">
                <div className={`text-2xl font-extrabold font-mono ${activeStyle.color} flex items-center gap-2`}>
                  {activeStyle.label}
                </div>
                <div className="text-right">
                  <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Confidence</span>
                  <div className="text-2xl font-bold font-mono text-white">
                    {Math.round((currentResult?.confidence || 0) * 1000) / 10}%
                  </div>
                </div>
              </div>
            </div>

            {/* Latency & Device metadata */}
            <div className="flex items-center justify-between py-2.5 px-3.5 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs font-mono">
              <span className="text-slate-400">Inference Latency:</span>
              <span className="text-emerald-400 font-bold">{currentResult?.latency || 18} ms</span>
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
                    {Math.round((currentResult?.probabilities?.positive || 0) * 1000) / 10}%
                  </span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div
                    style={{ width: `${(currentResult?.probabilities?.positive || 0) * 100}%` }}
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
                    {Math.round((currentResult?.probabilities?.neutral || 0) * 1000) / 10}%
                  </span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div
                    style={{ width: `${(currentResult?.probabilities?.neutral || 0) * 100}%` }}
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
                    {Math.round((currentResult?.probabilities?.negative || 0) * 1000) / 10}%
                  </span>
                </div>
                <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div
                    style={{ width: `${(currentResult?.probabilities?.negative || 0) * 100}%` }}
                    className="h-full bg-rose-500 transition-all duration-500 ease-out"
                  />
                </div>
              </div>
            </div>

            {/* Architecture Details Footer */}
            <div className="pt-4 border-t border-slate-800/80 text-[11px] font-mono text-slate-400 space-y-1">
              <div className="flex justify-between">
                <span>Architecture:</span>
                <span className="text-slate-200 font-semibold">
                  {mode === 'entity' ? 'Sentence-Pair Cross-Attention BERT' : '12-layer Transformer (BERT-base)'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Sequence Encoding:</span>
                <span className="text-cyan-300 font-mono">
                  {mode === 'entity' ? '[CLS] Target [SEP] Headline [SEP]' : '[CLS] Sentence [SEP]'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Fine-tuned Dataset:</span>
                <span className="text-slate-200">
                  {mode === 'entity' ? 'SEntFiN 1.0 (14,405 Pairs)' : 'Financial PhraseBank (3,453 Sentences)'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
