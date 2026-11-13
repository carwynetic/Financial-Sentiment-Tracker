import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arrow
import os

# Set publication-quality figure parameters
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 0.8

# Canvas setup - 16:9 ratio suitable for presentation slides
fig, ax = plt.subplots(figsize=(14, 7.5), dpi=300)
ax.set_xlim(0, 140)
ax.set_ylim(0, 75)
ax.axis('off')

# Academic Color Palette (Muted, Professional, Okabe-Ito inspired)
BG_STAGE = "#F8FAFC"       # Very light slate/white
BORDER_STAGE = "#CBD5E1"   # Soft slate border
TITLE_COLOR = "#0F172A"    # Deep slate for primary headings
SUB_COLOR = "#334155"      # Muted slate for body
ACCENT_BLUE = "#1E40AF"    # Academic Navy
ACCENT_TEAL = "#0F766E"    # Deep Teal
ACCENT_AMBER = "#B45309"   # Muted Amber/Rust
BOX_FILL_1 = "#F0F4F8"     # Soft light blue-gray
BOX_FILL_2 = "#F1F5F9"     # Neutral light gray
BOX_FILL_3 = "#EFF6FF"     # Subtle blue tint
BOX_FILL_4 = "#F0FDF4"     # Subtle green tint
BOX_BORDER = "#94A3B8"     # Border for internal cards

# Header
ax.text(70, 71.5, "SYSTEM ARCHITECTURE: FINANCIAL SENTIMENT TRACKER", 
        ha='center', va='center', fontsize=14, fontweight='bold', color=TITLE_COLOR)
ax.text(70, 69.0, "End-to-End Pipeline: From Raw Financial News to Entity-Aware Decision Intelligence", 
        ha='center', va='center', fontsize=9.5, style='italic', color='#64748B')

# Column dimensions
col_w = 30
col_h = 58
col_y = 7
gap = 4.5
start_x = 4

stages = [
    {
        "num": "STAGE 1",
        "title": "Data Ingestion & Cleaning",
        "color": "#1E3A8A",
        "bg": BOX_FILL_1,
        "x": start_x,
        "cards": [
            {
                "title": "Data Sources",
                "items": [
                    "• Financial PhraseBank (3,453 sentences)",
                    "• SEntFiN 1.0 (4,987 entity-headline pairs)",
                    "• Real-time Financial APIs (yfinance / RSS)"
                ]
            },
            {
                "title": "Domain Text Cleaner (cleaner.py)",
                "items": [
                    "• Preserves Currency: $, €, £, VND",
                    "• Retains Financial Numerics & % rates",
                    "• Retains Negative Verbs: loss, dropped",
                    "• Normalizes Whitespace & HTML entities"
                ]
            },
            {
                "title": "Token Representation",
                "items": [
                    "• WordPiece Tokenization (FinBERT Vocab)",
                    "• Fixed Sequence Length: max_len = 64",
                    "• VRAM Optimization: -75% memory footprint"
                ]
            }
        ]
    },
    {
        "num": "STAGE 2",
        "title": "Model Evaluation Hierarchy",
        "color": "#0F766E",
        "bg": BOX_FILL_2,
        "x": start_x + (col_w + gap),
        "cards": [
            {
                "title": "Tier 1: Lexicon Baseline",
                "items": [
                    "• Loughran-McDonald (2011/2025)",
                    "• Financial Sentiment Dictionary",
                    "• Macro-F1: 43.52% (Vocabulary Collision)"
                ]
            },
            {
                "title": "Tier 2: Classical ML",
                "items": [
                    "• TF-IDF Vectorization (n-gram (1,2))",
                    "• Multinomial Naive Bayes (F1: 53.87%)",
                    "• Logistic Regression (F1: 81.23%)",
                    "• Linear SVM Champion (F1: 81.29%)"
                ]
            },
            {
                "title": "Tier 3: Domain Transformer",
                "items": [
                    "• FinBERT Pre-trained (ProsusAI & HKUST)",
                    "• 12-layer Transformer, 768 hidden dim",
                    "• Financial Domain-Specific Corpus"
                ]
            }
        ]
    },
    {
        "num": "STAGE 3",
        "title": "Optimization & Disambiguation",
        "color": "#7C2D12",
        "bg": BOX_FILL_3,
        "x": start_x + (col_w + gap) * 2,
        "cards": [
            {
                "title": "Inverse Class Weighting (WCE)",
                "items": [
                    "• Tackles Severe Imbalance (62% Neutral)",
                    "• w_neg = 2.74  |  w_neu = 0.54  |  w_pos = 1.30",
                    "• Loss: L_WCE = -∑ w_c * y_c * log(p_c)",
                    "• Boosts Negative Class Recall (+13.45%)"
                ]
            },
            {
                "title": "Cross-Attention Entity Pair",
                "items": [
                    "• Target Entity + News Headline Pair",
                    "• [CLS] + Entity + [SEP] + Headline + [SEP]",
                    "• Segment IDs: [0...0, 1...1]",
                    "• Disambiguates Multi-Entity Conflicts"
                ]
            },
            {
                "title": "Training Strategy",
                "items": [
                    "• Stratified 70 / 15 / 15 Headline-Level Split",
                    "• GPU Mixed Precision (AMP fp16)",
                    "• AdamW Optimizer, Linear Warmup 10%"
                ]
            }
        ]
    },
    {
        "num": "STAGE 4",
        "title": "Inference & Deployment",
        "color": "#14532D",
        "bg": BOX_FILL_4,
        "x": start_x + (col_w + gap) * 3,
        "cards": [
            {
                "title": "Production Inference Engine",
                "items": [
                    "• High-Performance FastAPI Service",
                    "• Dual Endpoints: Sentence & Entity-Aware",
                    "• Model Warmup & TorchScript / GPU Caching",
                    "• Latency: 18.2ms (p95) on RTX 3050"
                ]
            },
            {
                "title": "Interactive Client Ecosystem",
                "items": [
                    "• React Web Terminal 2.0 (Dual-Mode UI)",
                    "• Chrome Extension V3 (Real-time Scraping)",
                    "• Automated Batch Benchmark Harness",
                    "• 34/34 Test Suite Passed (CI/CD Ready)"
                ]
            },
            {
                "title": "Evaluation & Validation",
                "items": [
                    "• Sentence Macro-F1: 89.76% (+8.47% vs SVM)",
                    "• Entity-Aware Macro-F1: 84.11%",
                    "• McNemar Significance: p = 0.0021 < 0.01"
                ]
            }
        ]
    }
]

# Draw stages and cards
for st_idx, st in enumerate(stages):
    x = st["x"]
    
    # Outer container box
    container = FancyBboxPatch((x, col_y), col_w, col_h,
                               boxstyle="round,pad=0.2,rounding_size=1.2",
                               facecolor=st["bg"], edgecolor=BORDER_STAGE, linewidth=1.2, zorder=1)
    ax.add_patch(container)
    
    # Stage header banner
    banner = FancyBboxPatch((x + 0.8, col_y + col_h - 6.5), col_w - 1.6, 5.5,
                            boxstyle="round,pad=0.1,rounding_size=0.8",
                            facecolor=st["color"], edgecolor="none", zorder=2)
    ax.add_patch(banner)
    
    # Stage header text
    ax.text(x + col_w/2, col_y + col_h - 2.8, st["num"],
            ha='center', va='center', fontsize=7.5, fontweight='bold', color="#93C5FD", zorder=3)
    ax.text(x + col_w/2, col_y + col_h - 4.7, st["title"],
            ha='center', va='center', fontsize=8.5, fontweight='bold', color="#FFFFFF", zorder=3)
    
    # Draw internal cards
    card_y = col_y + col_h - 8.5
    card_h = 15.5
    card_gap = 1.3
    
    for c_idx, card in enumerate(st["cards"]):
        cy = card_y - (c_idx + 1) * card_h - c_idx * card_gap + 1.2
        
        # Card background
        c_patch = FancyBboxPatch((x + 1.2, cy), col_w - 2.4, card_h,
                                 boxstyle="round,pad=0.1,rounding_size=0.6",
                                 facecolor="#FFFFFF", edgecolor=BOX_BORDER, linewidth=0.7, zorder=2)
        ax.add_patch(c_patch)
        
        # Card Title
        ax.text(x + 2.4, cy + card_h - 2.0, card["title"],
                ha='left', va='center', fontsize=8.2, fontweight='bold', color=TITLE_COLOR, zorder=3)
        
        # Card Items
        item_y = cy + card_h - 4.2
        for item in card["items"]:
            # Bold check for key metrics
            weight = 'normal'
            color = SUB_COLOR
            if "Macro-F1" in item or "w_neg" in item or "Latency" in item or "p = 0.0021" in item:
                color = "#0F172A"
                weight = 'bold'
                
            ax.text(x + 2.5, item_y, item,
                    ha='left', va='center', fontsize=6.8, fontweight=weight, color=color, zorder=3)
            item_y -= 2.6

    # Draw inter-stage arrow
    if st_idx < len(stages) - 1:
        arrow_x = x + col_w + 0.6
        arrow_y = col_y + col_h / 2
        ax.annotate("", xy=(arrow_x + gap - 1.2, arrow_y), xytext=(arrow_x, arrow_y),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6",
                                    color="#64748B", lw=1.8), zorder=5)

# Save figure in high-res PNG and PDF
out_dir = r"d:\Vscode-luyện code\Financial Sentiment Tracker (FinBERT Powered)\docs"
os.makedirs(out_dir, exist_ok=True)
png_path = os.path.join(out_dir, "system_architecture.png")
pdf_path = os.path.join(out_dir, "system_architecture.pdf")

# Also save directly into Google Drive for immediate access
gdrive_dir = r"G:\My Drive\Study\FPT University AI\Kì 5\Text Mining (TMG301)\Project"
gdrive_png = os.path.join(gdrive_dir, "system_architecture.png")

plt.tight_layout()
plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
plt.savefig(pdf_path, bbox_inches='tight', facecolor='#FFFFFF')
if os.path.exists(gdrive_dir):
    plt.savefig(gdrive_png, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')

print(f"Diagram successfully saved to:")
print(f"1. {png_path}")
print(f"2. {pdf_path}")
if os.path.exists(gdrive_dir):
    print(f"3. {gdrive_png}")
