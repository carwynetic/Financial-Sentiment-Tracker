import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import MarketPulse from './components/MarketPulse';
import AiSandbox from './components/AiSandbox';
import BenchmarkShowcase from './components/BenchmarkShowcase';
import ErrorTaxonomy from './components/ErrorTaxonomy';
import Footer from './components/Footer';
import { checkServerHealth } from './services/api';
import { TrendingUp, TrendingDown, MinusCircle, ShieldCheck, Sparkles } from 'lucide-react';

const ROLLING_TICKERS = [
  { symbol: 'AAPL', sentiment: 'BULLISH', score: '94.1%', change: '+1.8%', up: true },
  { symbol: 'NVDA', sentiment: 'BULLISH', score: '98.5%', change: '+4.2%', up: true },
  { symbol: 'TSLA', sentiment: 'BULLISH', score: '95.2%', change: '+2.4%', up: true },
  { symbol: 'MSFT', sentiment: 'NEUTRAL', score: '82.3%', change: '+0.1%', neutral: true },
  { symbol: 'AMZN', sentiment: 'BULLISH', score: '91.7%', change: '+1.5%', up: true },
  { symbol: 'GOOGL', sentiment: 'BULLISH', score: '88.9%', change: '+0.9%', up: true },
  { symbol: 'META', sentiment: 'BEARISH', score: '84.6%', change: '-1.2%', up: false }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('pulse');
  const [health, setHealth] = useState({
    online: false,
    latency: null,
    device: 'Loading...',
    model_loaded: false,
    model_source: 'FinBERT'
  });

  const pollHealth = async () => {
    const res = await checkServerHealth();
    setHealth(res);
  };

  useEffect(() => {
    pollHealth();
    const interval = setInterval(pollHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-obsidian-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Bloomberg-style Cyber Rolling Ticker Tape */}
      <div className="bg-obsidian-900 border-b border-slate-800/80 overflow-hidden py-1 px-4 text-[11px] font-mono">
        <div className="flex items-center gap-6 overflow-x-auto scrollbar-none whitespace-nowrap">
          <span className="text-slate-500 font-bold uppercase tracking-wider text-[10px] flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
            FINANCIAL SENTIMENT TAPE:
          </span>
          {ROLLING_TICKERS.map((ticker, idx) => (
            <div key={idx} className="flex items-center gap-1.5">
              <span className="text-white font-bold">${ticker.symbol}</span>
              <span
                className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                  ticker.sentiment === 'BULLISH'
                    ? 'text-emerald-400 bg-emerald-500/10'
                    : ticker.sentiment === 'BEARISH'
                    ? 'text-rose-400 bg-rose-500/10'
                    : 'text-slate-300 bg-slate-800'
                }`}
              >
                {ticker.sentiment} ({ticker.score})
              </span>
              <span className={`text-[10px] ${ticker.up ? 'text-emerald-400' : ticker.neutral ? 'text-slate-400' : 'text-rose-400'}`}>
                {ticker.change}
              </span>
              {idx < ROLLING_TICKERS.length - 1 && <span className="text-slate-700 ml-2">|</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Main Header with Telemetry & Tabs */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} health={health} />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'pulse' && <MarketPulse />}
        {activeTab === 'sandbox' && <AiSandbox />}
        {activeTab === 'benchmark' && <BenchmarkShowcase />}
        {activeTab === 'taxonomy' && <ErrorTaxonomy />}
      </main>

      {/* Accreditation Footer */}
      <Footer />
    </div>
  );
}
