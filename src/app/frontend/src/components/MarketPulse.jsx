import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, TrendingDown, MinusCircle, Search, ExternalLink, 
  RefreshCw, BarChart3, Newspaper, ShieldAlert, Sparkles 
} from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { fetchTickerSentiment } from '../services/api';

const QUICK_TICKERS = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'AMZN', 'GOOGL'];

const SENTIMENT_COLORS = {
  positive: '#10b981', // Emerald
  neutral: '#94a3b8',  // Slate Platinum
  negative: '#ef4444'  // Crimson
};

export default function MarketPulse() {
  const [selectedTicker, setSelectedTicker] = useState('AAPL');
  const [inputTicker, setInputTicker] = useState('AAPL');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const loadTicker = async (symbol) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchTickerSentiment(symbol);
      setData(res);
      setSelectedTicker(symbol);
    } catch (err) {
      setError('Unable to fetch live news stream. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTicker('AAPL');
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (inputTicker.trim()) {
      loadTicker(inputTicker.trim().toUpperCase());
    }
  };

  // Prepare chart data
  const chartData = data?.summary
    ? [
        { name: 'Bullish (Positive)', value: data.summary.bullish, color: SENTIMENT_COLORS.positive },
        { name: 'Neutral', value: data.summary.neutral, color: SENTIMENT_COLORS.neutral },
        { name: 'Bearish (Negative)', value: data.summary.bearish, color: SENTIMENT_COLORS.negative }
      ].filter((item) => item.value > 0)
    : [];

  const pulseStyles = {
    BULLISH: {
      border: 'border-emerald-500/40',
      bg: 'bg-emerald-950/20',
      text: 'text-emerald-400',
      glow: 'shadow-bullish-glow',
      icon: TrendingUp,
      label: 'BULLISH MOMENTUM'
    },
    BEARISH: {
      border: 'border-rose-500/40',
      bg: 'bg-rose-950/20',
      text: 'text-rose-400',
      glow: 'shadow-bearish-glow',
      icon: TrendingDown,
      label: 'BEARISH PRESSURE'
    },
    NEUTRAL: {
      border: 'border-slate-700/60',
      bg: 'bg-slate-900/40',
      text: 'text-slate-300',
      glow: 'shadow-cyber-sm',
      icon: MinusCircle,
      label: 'NEUTRAL SENTIMENT'
    }
  };

  const currentPulse = pulseStyles[data?.market_pulse] || pulseStyles.NEUTRAL;
  const PulseIcon = currentPulse.icon;

  return (
    <div className="space-y-6">
      {/* Search & Quick Ticker Bar */}
      <div className="glass-panel rounded-2xl p-4 sm:p-5 flex flex-col md:flex-row items-center justify-between gap-4">
        <form onSubmit={handleSearch} className="flex items-center gap-2 w-full md:w-auto flex-1 max-w-md">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={inputTicker}
              onChange={(e) => setInputTicker(e.target.value.toUpperCase())}
              placeholder="Search ticker symbol (e.g. AAPL, NVDA)..."
              className="w-full pl-10 pr-4 py-2 bg-slate-900/80 border border-slate-700/80 rounded-xl text-sm font-mono tracking-wider text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-medium transition-all shadow-cyber-sm flex items-center gap-1.5 disabled:opacity-50"
          >
            {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4 text-cyan-300" />}
            <span>Analyze</span>
          </button>
        </form>

        {/* Quick Tickers */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto scrollbar-none">
          <span className="text-xs text-slate-400 font-mono hidden sm:inline mr-1">QUICK:</span>
          {QUICK_TICKERS.map((symbol) => (
            <button
              key={symbol}
              onClick={() => {
                setInputTicker(symbol);
                loadTicker(symbol);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
                selectedTicker === symbol
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-cyber-sm'
                  : 'bg-slate-800/60 text-slate-300 hover:bg-slate-700/60 border border-slate-700/40'
              }`}
            >
              ${symbol}
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid: Market Pulse Card + Donut Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Market Pulse Banner & Summary */}
        <div className={`lg:col-span-2 glass-panel rounded-2xl p-6 border ${currentPulse.border} ${currentPulse.bg} ${currentPulse.glow} relative overflow-hidden transition-all duration-300`}>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-3xl font-extrabold tracking-tight text-white font-mono">
                  ${data?.symbol || selectedTicker}
                </span>
                <span className={`px-2.5 py-1 rounded-full text-xs font-mono font-bold tracking-wider flex items-center gap-1.5 ${currentPulse.bg} ${currentPulse.text} border ${currentPulse.border}`}>
                  <PulseIcon className="w-3.5 h-3.5" />
                  {currentPulse.label}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">
                Real-Time Financial Sentiment Ingestion • FinBERT 768-dim Embedding
              </p>
            </div>

            <button
              onClick={() => loadTicker(selectedTicker)}
              disabled={loading}
              className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200 self-start sm:self-auto bg-slate-900/60 px-3 py-1.5 rounded-lg border border-slate-800"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>Refresh Stream</span>
            </button>
          </div>

          {/* Metric Stats Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
            <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-3.5">
              <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Bullish Ratio</span>
              <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
                {data?.summary?.total ? `${Math.round((data.summary.bullish / data.summary.total) * 100)}%` : '0%'}
              </div>
              <span className="text-[10px] text-slate-500 font-mono">{data?.summary?.bullish || 0} Articles</span>
            </div>

            <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-3.5">
              <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Bearish Ratio</span>
              <div className="text-2xl font-bold font-mono text-rose-400 mt-1">
                {data?.summary?.total ? `${Math.round((data.summary.bearish / data.summary.total) * 100)}%` : '0%'}
              </div>
              <span className="text-[10px] text-slate-500 font-mono">{data?.summary?.bearish || 0} Articles</span>
            </div>

            <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-3.5">
              <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Neutral Ratio</span>
              <div className="text-2xl font-bold font-mono text-slate-300 mt-1">
                {data?.summary?.total ? `${Math.round((data.summary.neutral / data.summary.total) * 100)}%` : '0%'}
              </div>
              <span className="text-[10px] text-slate-500 font-mono">{data?.summary?.neutral || 0} Articles</span>
            </div>

            <div className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-3.5">
              <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Total Scraped</span>
              <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">
                {data?.summary?.total || 0}
              </div>
              <span className="text-[10px] text-slate-500 font-mono">Live Ingested</span>
            </div>
          </div>

          {/* Progress Stack Bar */}
          {data?.summary?.total > 0 && (
            <div className="w-full bg-slate-800/80 rounded-full h-2.5 overflow-hidden flex">
              <div
                style={{ width: `${(data.summary.bullish / data.summary.total) * 100}%` }}
                className="bg-emerald-500 transition-all duration-500"
              />
              <div
                style={{ width: `${(data.summary.neutral / data.summary.total) * 100}%` }}
                className="bg-slate-500 transition-all duration-500"
              />
              <div
                style={{ width: `${(data.summary.bearish / data.summary.total) * 100}%` }}
                className="bg-rose-500 transition-all duration-500"
              />
            </div>
          )}
        </div>

        {/* Right: Interactive Donut Chart */}
        <div className="glass-panel rounded-2xl p-5 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-mono font-semibold tracking-wider text-slate-300 uppercase flex items-center gap-1.5">
              <BarChart3 className="w-3.5 h-3.5 text-cyan-400" />
              Sentiment Share
            </h3>
            <span className="text-[10px] font-mono text-slate-500">FPB Calibrated</span>
          </div>

          <div className="h-44 w-full flex items-center justify-center relative">
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Tooltip
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        return (
                          <div className="bg-obsidian-950 border border-slate-700 p-2.5 rounded-lg shadow-xl text-xs font-mono">
                            <p className="text-white font-bold">{payload[0].name}</p>
                            <p className="text-cyan-400">{payload[0].value} headlines</p>
                          </div>
                        );
                      }
                      return null;
                    }}
                  />
                  <Pie
                    data={chartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={48}
                    outerRadius={68}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} stroke="#0B0F17" strokeWidth={2} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-xs text-slate-500 font-mono">No data points</div>
            )}
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-xs font-mono text-slate-400 uppercase">Pulse</span>
              <span className="text-sm font-bold font-mono text-white">{data?.market_pulse || 'NEUTRAL'}</span>
            </div>
          </div>

          <div className="flex justify-around text-[11px] font-mono pt-3 border-t border-slate-800">
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <span className="text-slate-300">Bullish</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-slate-400"></span>
              <span className="text-slate-300">Neutral</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              <span className="text-slate-300">Bearish</span>
            </div>
          </div>
        </div>
      </div>

      {/* Live News Stream Section */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Newspaper className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-semibold tracking-wide text-white uppercase font-mono">
              Live Ingested Financial Feed ({data?.articles?.length || 0})
            </h3>
          </div>
          <span className="text-xs font-mono text-slate-400">
            Source: <strong className="text-slate-200">Yahoo Finance Live / Reuters / Bloomberg</strong>
          </span>
        </div>

        {loading ? (
          <div className="glass-panel rounded-2xl p-12 text-center">
            <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin mx-auto mb-3" />
            <p className="text-sm text-slate-300 font-mono">Scraping live articles and running FinBERT GPU inference...</p>
          </div>
        ) : data?.articles?.length ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.articles.map((item, idx) => {
              const isPositive = item.sentiment === 'positive';
              const isNegative = item.sentiment === 'negative';
              const badgeBg = isPositive
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                : isNegative
                ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                : 'bg-slate-700/20 text-slate-300 border-slate-600/30';

              const confPct = Math.round(item.confidence * 100);

              return (
                <div
                  key={idx}
                  className="glass-panel glass-panel-hover rounded-xl p-4 flex flex-col justify-between border border-slate-800/80 bg-slate-900/40 relative group"
                >
                  <div>
                    {/* Card Top: Sentiment Pill + Confidence */}
                    <div className="flex items-center justify-between gap-2 mb-2.5">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold tracking-wider uppercase border ${badgeBg}`}>
                        {item.sentiment}
                      </span>
                      <span className="text-xs font-mono text-slate-400">
                        Confidence: <strong className="text-white">{confPct}%</strong>
                      </span>
                    </div>

                    {/* Headline Title */}
                    <h4 className="text-sm font-medium text-slate-100 group-hover:text-cyan-300 transition-colors leading-snug mb-3">
                      "{item.title}"
                    </h4>
                  </div>

                  {/* Card Bottom: Publisher + Source Link + Prob Bar */}
                  <div className="pt-3 border-t border-slate-800/60">
                    <div className="flex items-center justify-between text-xs mb-2">
                      <span className="text-slate-400 font-mono flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
                        {item.publisher || 'Financial Press'}
                      </span>
                      {item.link ? (
                        <a
                          href={item.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-mono text-[11px]"
                        >
                          <span>Read Source</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      ) : (
                        <span className="text-slate-500 text-[10px] font-mono">Wire News</span>
                      )}
                    </div>

                    {/* Mini Probabilities Bar */}
                    {item.probabilities && (
                      <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden flex">
                        <div
                          style={{ width: `${(item.probabilities.positive || 0) * 100}%` }}
                          className="bg-emerald-500"
                        />
                        <div
                          style={{ width: `${(item.probabilities.neutral || 0) * 100}%` }}
                          className="bg-slate-500"
                        />
                        <div
                          style={{ width: `${(item.probabilities.negative || 0) * 100}%` }}
                          className="bg-rose-500"
                        />
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="glass-panel rounded-2xl p-8 text-center text-slate-400 font-mono text-sm">
            No live news found for ${selectedTicker}. Try searching another ticker like AAPL or NVDA.
          </div>
        )}
      </div>
    </div>
  );
}
