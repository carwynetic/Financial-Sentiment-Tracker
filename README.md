# 📈 Financial Sentiment Tracker (FinBERT Powered)

> **Next-Gen Cyber FinTech Terminal & Target-Oriented Financial Sentiment Intelligence System**  
> *Course: Text Mining (TMG301) – AI Batch 19, FPT University*  
> *Supervisor: ThS. Vũ Hà Anh*  
> *Authors (Group 4 - Antigravity): Nguyễn Đoàn Bảo Phúc (Lead), Nguyễn Phú Triệu, Ngô Công Minh, Nguyễn Công Minh*

---

## 🎯 1. Overview & Motivation

Financial markets operate on high-frequency news narratives, SEC regulatory filings, and corporate earnings disclosures. Standard general-domain NLP models and sentiment lexicons consistently fail in financial text mining due to domain-specific linguistic barriers:

1. **Accounting Vocabulary Collision**: As proven by *Loughran & McDonald (2011)* on *The Journal of Finance*, general sentiment lexicons (like VADER or Harvard GI) misclassify over **73.8%** of negative words in financial reports. Standard terms such as `"liability"`, `"cost"`, `"tax"`, and `"depreciation"` are neutral accounting necessities, yet standard tools mislabel them as negative.
2. **Multi-Entity Sentiment Conflict**: Headlines routinely reference multiple companies with opposing market momentum (e.g., *"Gold extends gains on festive buying, weak rupee"*). Traditional sentence-level classifiers collapse to a neutral average, destroying trading signals (*SEntFiN 1.0 - Sinha et al., ACL 2022*).
3. **Severe Class Imbalance**: Financial news is naturally dominated by Neutral statements (> 62%), making raw Accuracy deceptive.

This project delivers an end-to-end research-backed system featuring a **Tri-Tier Benchmarking Ladder**, **Paired McNemar Statistical Hypothesis Testing ($p < 0.01$)**, **Entity-Aware Cross-Attention Modeling**, a high-performance **FastAPI GPU Microservice (< 20ms)**, a **Bloomberg Terminal 2.0 Web Dashboard (React 19 + TailwindCSS)**, and a **Chrome Browser Extension (Manifest V3)**.

---

## 🔬 2. Master Benchmark Results

All models were evaluated on the fixed, un-leaked Test Set ($N = 518$, 15% Stratified Split) of the **Financial PhraseBank (75% Agreement)** benchmark (*Malo et al., 2014*), and the entity extension on **SEntFiN 1.0 Test Set** ($N = 2,169$).

| Paradigm | Model Architecture | Accuracy | Macro P | Macro R | Macro F1 | Weighted F1 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Tier 1: Lexicon** | Loughran-McDonald Master Dict (1993–2025) | 56.18% | 44.01% | 43.54% | 43.52% | 55.58% |
| **Tier 2: Classical ML** | Multinomial Naive Bayes (TF-IDF 10k) | 74.71% | 80.40% | 52.60% | 53.87% | 70.20% |
| **Tier 2: Classical ML** | Logistic Regression (Class-Balanced) | 85.71% | 84.63% | 78.68% | 81.23% | 85.38% |
| **Tier 2: Classical ML** | **Linear SVM (Tier 2 Champion)** | **86.49%** | **87.88%** | **77.24%** | **81.29%** | **85.91%** |
| **Tier 3: Transformer (ZS)** | FinBERT Zero-Shot (HKUST) | 88.42% | 89.11% | 84.22% | 86.22% | 88.06% |
| **Tier 3: Transformer (FT)** | **FinBERT Fine-Tuned (HKUST + Class Weights)** | **92.08%** | **88.97%** | **90.69%** | **89.76%** | **92.10%** |
| **Tier 3: Transformer (ZS)** | FinBERT Zero-Shot (ProsusAI) | 97.10% | 95.43% | 98.02% | 96.64% | 97.13% |
| **Extension: Multi-Entity** | **Entity-FinBERT (SEntFiN 1.0 Benchmark)** | **84.09%** | **84.31%** | **83.94%** | **84.11%** | **84.09%** |

### 📊 Statistical Significance (McNemar's Test with Edwards' Correction)
Between **FinBERT Fine-Tuned** and the strongest baseline (**Linear SVM**):
$$\chi^2 = \frac{(|b - c| - 1)^2}{b + c} = \frac{(|56 - 27| - 1)^2}{56 + 27} = \frac{784}{83} \approx 9.4458 \quad (p = 0.0021 < 0.01)$$
* **Conclusion**: FinBERT correctly classified 56 test samples where Linear SVM failed, while Linear SVM only succeeded on 27 samples where FinBERT erred. The null hypothesis of marginal homogeneity is statistically rejected ($p < 0.01$), proving the performance delta is significant and not due to random variation.

---

## 🛠️ 3. System Architecture & Components

```
Financial Sentiment Tracker
├── 🧠 Deep Learning Engine (PyTorch, Transformers, FinBERT)
│   ├── Inverse Class-Weighted Loss (w_neg=2.74, w_neu=0.54, w_pos=1.30)
│   ├── AMP (Automatic Mixed Precision fp16) on NVIDIA RTX 3050 Laptop GPU
│   └── Sentence-Pair Cross-Attention: [CLS] Target [SEP] Headline [SEP]
├── ⚡ Backend Microservice (FastAPI + Uvicorn)
│   ├── Lifespan GPU Warmup & VRAM Management
│   ├── Endpoints: /health, /predict/sentiment, /predict/batch, /ticker/{symbol}
│   └── Real-time Financial News Scraper & Market Pulse Aggregator (yfinance)
├── 🖥️ Web SPA Dashboard (React 19 + TailwindCSS + Recharts)
│   ├── Cyber Bloomberg Terminal 2.0 Dark Interface (#080B10)
│   ├── Real-time Ticker Search & Sentiment Donut Visualizer
│   └── Directly served by FastAPI ASGI without external Node.js server
└── 🧩 Chrome Browser Extension (Manifest V3)
    ├── Right-click Context Menu ("⚡ Phân tích cảm xúc với FinBERT")
    └── Real-time Popup with Confidence Gauge & Response Latency Meter (< 20ms)
```

---

## 📁 4. Project Directory Structure

```text
├── data/
│   ├── processed/             # Parquet & CSV splits (train, val, test, sentfin)
│   └── raw/                   # Raw benchmark datasets
├── extension/                 # Chrome Browser Extension (Manifest V3)
│   ├── background.js          # Service worker & context menu listener
│   ├── manifest.json          # Manifest V3 specification
│   ├── popup.html             # Extension GUI
│   └── popup.js               # API caller & live gauge renderer
├── models/                    # Model configs, tokenizers, joblib baselines
│   ├── finbert_best/          # Best fine-tuned FinBERT config & tokenizers
│   └── finbert_entity_best/   # SEntFiN entity-aware model configs
├── notebooks/                 # 01_exploratory_data_analysis.ipynb
├── reports/                   # Academic deliverables & figures
│   ├── figures/               # Normalized confusion matrices & distributions
│   ├── metrics/               # Frozen metrics JSON files
│   ├── tables/                # Benchmark tables in CSV, Markdown, LaTeX
│   ├── TMG301_Project_Final_Report.docx  # Full comprehensive Word report
│   └── TMG301_Project_Final_Report.pdf   # Formatted academic PDF report
├── src/
│   ├── app/                   # FastAPI app & React frontend source
│   │   ├── frontend/          # React 19 + TailwindCSS SPA codebase
│   │   └── main.py            # Microservice API & integrated SPA server
│   ├── data/                  # Dataset download & stratified split scripts
│   ├── evaluation/            # McNemar test, error taxonomy & table generator
│   ├── models/                # Training & evaluation scripts (ML & Transformers)
│   └── preprocessing/         # FinancialTextCleaner regex pipeline
├── tests/                     # Automated test suite (31/31 Unit Tests PASSED)
├── .gitignore                 # Safe git exclusion rules
├── README.md                  # Project documentation (this file)
└── requirements.txt           # Python dependency manifest
```

---

## 🚀 5. Quickstart Guide

### 1. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/carwynetic/Financial-Sentiment-Tracker.git
cd Financial-Sentiment-Tracker

# Install dependencies
pip install -r requirements.txt
```

> **Note on Weights**: Large transformer weights (`*.safetensors` > 400MB) are ignored from GitHub by policy. The microservice automatically loads `models/finbert_best` if local weights exist, or seamlessly falls back to pre-trained weights from Hugging Face (`ProsusAI/finbert`).

### 2. Run All Automated Tests (31/31 PASSED)
Verify full system integrity (cleaner, lexicons, classical ML, FinBERT, McNemar, error analysis, and FastAPI endpoints):
```bash
python -m pytest tests/ -v -p no:cacheprovider
```

### 3. Launch Web Terminal & API (Single Command)
Run the unified FastAPI server. It serves both the backend API and the compiled React Bloomberg Terminal 2.0 Web SPA:
```bash
python -m uvicorn src.app.main:app --host 127.0.0.1 --port 8000
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:8000`**

### 4. Install Chrome Browser Extension (Manifest V3)
1. Open Google Chrome and go to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in the top-right corner).
3. Click **Load unpacked** and select the `extension/` folder inside this repository.
4. Highlight any financial news headline on Yahoo Finance, Bloomberg, or CafeF, right-click and choose **"⚡ Phân tích cảm xúc với FinBERT"**.

---

## 👥 6. Academic Team Allocation (RACI Matrix)

| Member | Main Role | Core Deliverables | Contribution |
| :--- | :--- | :--- | :---: |
| **Nguyễn Đoàn Bảo Phúc** | Team & Deep Learning Lead | FinBERT fine-tuning, SEntFiN entity-aware model, FastAPI backend | 25% |
| **Nguyễn Phú Triệu** | Baseline & Statistics Lead | Loughran-McDonald lexicon, TF-IDF classical ML, McNemar testing | 25% |
| **Ngô Công Minh** | Data & Preprocessing Lead | Stratified split, `cleaner.py` pipeline, EDA, data leakage audit | 25% |
| **Nguyễn Công Minh** | Application & Frontend Lead | React Bloomberg Terminal SPA, Chrome Extension V3, Documentation | 25% |

---

## 📜 7. License & Citation
Developed for academic research purposes under the **MIT License**.
If utilizing this benchmark pipeline or methodology, please cite:
* Araci, D. T. (2019). *FinBERT: Financial Sentiment Analysis with Pre-trained Language Models.* arXiv:1908.10063.
* Sinha, A., et al. (2022). *SEntFiN 1.0: Entity-aware sentiment analysis for financial news.* JASIST, 73(9), 1314–1335.
* Malo, P., et al. (2014). *Good debt or bad debt: Detecting semantic orientations in economic texts.* JASIST, 65(4), 782–796.
