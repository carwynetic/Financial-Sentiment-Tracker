/**
 * API Service for FinBERT Financial Sentiment Tracker
 * Target Server: http://127.0.0.1:8000
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

// Mock data fallback in case backend is offline or yfinance rate-limited
const MOCK_TICKERS = {
  AAPL: {
    symbol: 'AAPL',
    market_pulse: 'BULLISH',
    summary: { bullish: 4, bearish: 1, neutral: 2, total: 7 },
    articles: [
      {
        title: 'Apple reports record Services revenue and solid iPhone demand in Asian markets.',
        publisher: 'Reuters',
        link: 'https://www.reuters.com',
        sentiment: 'positive',
        confidence: 0.9412,
        probabilities: { positive: 0.9412, neutral: 0.0482, negative: 0.0106 }
      },
      {
        title: 'Morgan Stanley raises Apple price target to $240 citing AI feature rollout momentum.',
        publisher: 'Bloomberg',
        link: 'https://www.bloomberg.com',
        sentiment: 'positive',
        confidence: 0.9125,
        probabilities: { positive: 0.9125, neutral: 0.0712, negative: 0.0163 }
      },
      {
        title: 'Apple supplier Foxconn increases holiday production capacity by 12% in Zhengzhou.',
        publisher: 'CNBC',
        link: 'https://www.cnbc.com',
        sentiment: 'positive',
        confidence: 0.8841,
        probabilities: { positive: 0.8841, neutral: 0.1015, negative: 0.0144 }
      },
      {
        title: 'EU regulators examine App Store compliance terms under Digital Markets Act.',
        publisher: 'Financial Times',
        link: 'https://www.ft.com',
        sentiment: 'neutral',
        confidence: 0.7632,
        probabilities: { positive: 0.0821, neutral: 0.7632, negative: 0.1547 }
      },
      {
        title: 'Apple to hold annual shareholder meeting on February 28 to review quarterly dividend.',
        publisher: 'MarketWatch',
        link: 'https://www.marketwatch.com',
        sentiment: 'neutral',
        confidence: 0.8921,
        probabilities: { positive: 0.0512, neutral: 0.8921, negative: 0.0567 }
      },
      {
        title: 'Smartphone market faces short-term macroeconomic headwinds in European retail channels.',
        publisher: 'Wall Street Journal',
        link: 'https://www.wsj.com',
        sentiment: 'negative',
        confidence: 0.8245,
        probabilities: { positive: 0.0341, neutral: 0.1414, negative: 0.8245 }
      },
      {
        title: 'Operating cash flow reaches $39.9 billion driven by gross margin expansion.',
        publisher: 'Bloomberg',
        link: 'https://www.bloomberg.com',
        sentiment: 'positive',
        confidence: 0.9634,
        probabilities: { positive: 0.9634, neutral: 0.0311, negative: 0.0055 }
      }
    ]
  },
  TSLA: {
    symbol: 'TSLA',
    market_pulse: 'BULLISH',
    summary: { bullish: 3, bearish: 2, neutral: 1, total: 6 },
    articles: [
      {
        title: 'Tesla global deliveries surge 35% quarter-over-quarter as Model Y demand accelerates.',
        publisher: 'Reuters',
        link: 'https://www.reuters.com',
        sentiment: 'positive',
        confidence: 0.9521,
        probabilities: { positive: 0.9521, neutral: 0.0392, negative: 0.0087 }
      },
      {
        title: 'Tesla Energy Megapack deployments reach all-time high with strong margin profile.',
        publisher: 'Bloomberg',
        link: 'https://www.bloomberg.com',
        sentiment: 'positive',
        confidence: 0.9231,
        probabilities: { positive: 0.9231, neutral: 0.0641, negative: 0.0128 }
      },
      {
        title: 'Autonomous Full Self-Driving hardware 4.0 update rolls out across European fleets.',
        publisher: 'Electrek',
        link: 'https://electrek.co',
        sentiment: 'positive',
        confidence: 0.8145,
        probabilities: { positive: 0.8145, neutral: 0.1532, negative: 0.0323 }
      },
      {
        title: 'Intense price competition in Chinese EV sector squeezes gross automotive margins.',
        publisher: 'CNBC',
        link: 'https://www.cnbc.com',
        sentiment: 'negative',
        confidence: 0.8654,
        probabilities: { positive: 0.0412, neutral: 0.0934, negative: 0.8654 }
      },
      {
        title: 'Production pause scheduled at Berlin Gigafactory for scheduled retooling.',
        publisher: 'Reuters',
        link: 'https://www.reuters.com',
        sentiment: 'neutral',
        confidence: 0.7812,
        probabilities: { positive: 0.0911, neutral: 0.7812, negative: 0.1277 }
      },
      {
        title: 'Raw lithium and battery metal volatility introduces operational cost uncertainty.',
        publisher: 'Financial Times',
        link: 'https://www.ft.com',
        sentiment: 'negative',
        confidence: 0.7932,
        probabilities: { positive: 0.0612, neutral: 0.1456, negative: 0.7932 }
      }
    ]
  },
  NVDA: {
    symbol: 'NVDA',
    market_pulse: 'BULLISH',
    summary: { bullish: 5, bearish: 0, neutral: 1, total: 6 },
    articles: [
      {
        title: 'Nvidia Data Center revenue explodes 217% year-on-year propelled by Hopper and Blackwell AI architectures.',
        publisher: 'Reuters',
        link: 'https://www.reuters.com',
        sentiment: 'positive',
        confidence: 0.9854,
        probabilities: { positive: 0.9854, neutral: 0.0121, negative: 0.0025 }
      },
      {
        title: 'Hyperscalers expand multi-billion dollar capital expenditure plans for next-gen GPU clusters.',
        publisher: 'Bloomberg',
        link: 'https://www.bloomberg.com',
        sentiment: 'positive',
        confidence: 0.9312,
        probabilities: { positive: 0.9312, neutral: 0.0543, negative: 0.0145 }
      },
      {
        title: 'Operating margin broadens to record 65.4% amid premium enterprise pricing power.',
        publisher: 'Wall Street Journal',
        link: 'https://www.wsj.com',
        sentiment: 'positive',
        confidence: 0.9721,
        probabilities: { positive: 0.9721, neutral: 0.0241, negative: 0.0038 }
      },
      {
        title: 'Nvidia announces strategic partnership with major global telecommunications operators.',
        publisher: 'CNBC',
        link: 'https://www.cnbc.com',
        sentiment: 'positive',
        confidence: 0.8942,
        probabilities: { positive: 0.8942, neutral: 0.0981, negative: 0.0077 }
      },
      {
        title: 'Upcoming earnings call set for next Wednesday at 2:00 PM Pacific Time.',
        publisher: 'MarketWatch',
        link: 'https://www.marketwatch.com',
        sentiment: 'neutral',
        confidence: 0.9123,
        probabilities: { positive: 0.0411, neutral: 0.9123, negative: 0.0466 }
      },
      {
        title: 'Demand for Blackwell B200 accelerators completely sold out for next 12 months.',
        publisher: 'Reuters',
        link: 'https://www.reuters.com',
        sentiment: 'positive',
        confidence: 0.9678,
        probabilities: { positive: 0.9678, neutral: 0.0289, negative: 0.0033 }
      }
    ]
  }
};

export async function checkServerHealth() {
  const start = performance.now();
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2500);
    const res = await fetch(`${API_BASE_URL}/health`, {
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    const latency = Math.round(performance.now() - start);

    if (res.ok) {
      const data = await res.json();
      return {
        online: true,
        latency,
        device: data.device || 'cuda:0',
        model_loaded: data.model_loaded,
        model_source: data.model_source || 'FinBERT'
      };
    }
    throw new Error('Server returned non-200');
  } catch (err) {
    return {
      online: false,
      latency: Math.round(performance.now() - start),
      device: 'GPU Simulated (RTX 3050)',
      model_loaded: true,
      model_source: 'models/finbert_best',
      fallback: true
    };
  }
}

export async function predictSentiment(text) {
  const start = performance.now();
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);
    const res = await fetch(`${API_BASE_URL}/predict/sentiment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
      signal: controller.signal
    });
    clearTimeout(timeoutId);
    const latency = Math.round(performance.now() - start);

    if (res.ok) {
      const data = await res.json();
      return { ...data, latency, isFallback: false };
    }
    throw new Error('API request failed');
  } catch (err) {
    // Intelligent heuristic fallback if backend API is not currently started
    const latency = Math.round(performance.now() - start) + 16;
    const lower = text.toLowerCase();
    let sentiment = 'neutral';
    let conf = 0.88;
    let probs = { positive: 0.06, neutral: 0.88, negative: 0.06 };

    if (lower.includes('profit') || lower.includes('increase') || lower.includes('surged') || lower.includes('grew') || lower.includes('beat') || lower.includes('gain')) {
      sentiment = 'positive';
      conf = 0.9412;
      probs = { positive: 0.9412, neutral: 0.0482, negative: 0.0106 };
    } else if (lower.includes('loss') || lower.includes('drop') || lower.includes('plunge') || lower.includes('decline') || lower.includes('fall') || lower.includes('cut')) {
      if (lower.includes('narrowed') || lower.includes('swung to profit')) {
        // complex turnaround case
        sentiment = 'positive';
        conf = 0.8145;
        probs = { positive: 0.8145, neutral: 0.1245, negative: 0.0610 };
      } else {
        sentiment = 'negative';
        conf = 0.9184;
        probs = { positive: 0.0215, neutral: 0.0601, negative: 0.9184 };
      }
    }

    return {
      text,
      sentiment,
      confidence: conf,
      probabilities: probs,
      latency,
      isFallback: true
    };
  }
}

export async function fetchTickerSentiment(symbol) {
  const cleanSymbol = symbol.trim().toUpperCase();
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 6000);
    const res = await fetch(`${API_BASE_URL}/ticker/${cleanSymbol}`, {
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (res.ok) {
      const data = await res.json();
      return { ...data, isFallback: false };
    }
    throw new Error('Ticker fetch failed');
  } catch (err) {
    // Fallback to high-quality mock data for the requested ticker
    const fallbackData = MOCK_TICKERS[cleanSymbol] || {
      symbol: cleanSymbol,
      market_pulse: 'BULLISH',
      summary: { bullish: 3, bearish: 1, neutral: 1, total: 5 },
      articles: [
        {
          title: `${cleanSymbol} reports quarterly revenue growth surpassing Wall Street projections.`,
          publisher: 'Reuters',
          link: 'https://www.reuters.com',
          sentiment: 'positive',
          confidence: 0.9324,
          probabilities: { positive: 0.9324, neutral: 0.0542, negative: 0.0134 }
        },
        {
          title: `Key enterprise partners accelerate technology integration contracts with ${cleanSymbol}.`,
          publisher: 'Bloomberg',
          link: 'https://www.bloomberg.com',
          sentiment: 'positive',
          confidence: 0.8876,
          probabilities: { positive: 0.8876, neutral: 0.0982, negative: 0.0142 }
        },
        {
          title: `${cleanSymbol} executives discuss strategic capital allocation at annual investor summit.`,
          publisher: 'CNBC',
          link: 'https://www.cnbc.com',
          sentiment: 'neutral',
          confidence: 0.8145,
          probabilities: { positive: 0.0821, neutral: 0.8145, negative: 0.1034 }
        },
        {
          title: `Rising manufacturing input costs create minor margin pressure for ${cleanSymbol}.`,
          publisher: 'Wall Street Journal',
          link: 'https://www.wsj.com',
          sentiment: 'negative',
          confidence: 0.7891,
          probabilities: { positive: 0.0512, neutral: 0.1597, negative: 0.7891 }
        },
        {
          title: `Institutional hedge funds increase overweight portfolio allocations in ${cleanSymbol}.`,
          publisher: 'Financial Times',
          link: 'https://www.ft.com',
          sentiment: 'positive',
          confidence: 0.9102,
          probabilities: { positive: 0.9102, neutral: 0.0762, negative: 0.0136 }
        }
      ]
    };
    return { ...fallbackData, isFallback: true };
  }
}
