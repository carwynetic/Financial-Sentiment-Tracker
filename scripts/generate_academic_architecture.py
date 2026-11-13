import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# 1. Academic Publication Settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'mathtext.fontset': 'cm',  # Computer Modern LaTeX math
    'figure.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42
})

fig, ax = plt.subplots(figsize=(16, 8.6), dpi=300)
ax.set_xlim(0, 160)
ax.set_ylim(0, 86)
ax.axis('off')

# Professional Academic Palette (Nature/NeurIPS color scheme)
C_DARK = "#0F172A"       # Primary text
C_MUTED = "#475569"      # Secondary text / annotations
C_LIGHT_MUTED = "#64748B"# Small captions
C_CONTAINER = "#F8FAFC"  # Stage background

# Stage themes: Background, Border, Header Text, Header Fill
THEMES = [
    {"fill": "#FFFFFF", "bd": "#0284C7", "txt": "#0369A1", "hdr": "#E0F2FE", "box": "#F0F9FF"},  # Stage 1: Sky
    {"fill": "#FFFFFF", "bd": "#D97706", "txt": "#B45309", "hdr": "#FEF3C7", "box": "#FFFBEB"},  # Stage 2: Amber
    {"fill": "#FFFFFF", "bd": "#DC2626", "txt": "#B91C1C", "hdr": "#FEE2E2", "box": "#FEF2F2"},  # Stage 3: Rose
    {"fill": "#FFFFFF", "bd": "#16A34A", "txt": "#15803D", "hdr": "#DCFCE7", "box": "#F0FDF4"}   # Stage 4: Green
]

# -------------------------------------------------------------------------
# TOP BANNER: TITLE & ACADEMIC HEADER
# -------------------------------------------------------------------------
ax.text(80, 82.8, "Figure 1: End-to-End System Architecture for Entity-Aware Financial Sentiment Analysis",
        ha='center', va='center', fontsize=13.5, color=C_DARK, fontweight='bold')
ax.text(80, 80.2, "Raw Financial Stream  -->  Sentence-Pair Cross-Attention  -->  FinBERT Encoder  -->  Cost-Sensitive WCE Loss  -->  Production Serving",
        ha='center', va='center', fontsize=8.5, color=C_MUTED, style='italic')

# Top Stage Banners
stage_headers = [
    (4, 38, "Stage 1: Input & Embedding", "Financial Cleaner & Tokenizer", THEMES[0]),
    (42, 84, "Stage 2: Domain FinBERT Backbone", "12-Layer Transformer Encoder", THEMES[1]),
    (88, 122, "Stage 3: Head & Cost-Sensitive Loss", "Multi-Entity Disambiguation & WCE", THEMES[2]),
    (126, 156, "Stage 4: Production Deployment", "FastAPI & Client Ecosystem", THEMES[3])
]

for x1, x2, t1, t2, th in stage_headers:
    w = x2 - x1
    p = FancyBboxPatch((x1, 72.5), w, 4.4, boxstyle="round,pad=0.2,rounding_size=0.6",
                       facecolor=th["hdr"], edgecolor=th["bd"], linewidth=1.2)
    ax.add_patch(p)
    ax.text(x1 + w/2, 75.3, t1, ha='center', va='center', fontsize=8.5, color=th["txt"], fontweight='bold')
    ax.text(x1 + w/2, 73.6, t2, ha='center', va='center', fontsize=6.8, color=C_MUTED, style='italic')

# -------------------------------------------------------------------------
# STAGE 1: INPUT REPRESENTATION & EMBEDDINGS (x: 4 to 38)
# -------------------------------------------------------------------------
c1 = FancyBboxPatch((4, 4), 34, 66.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                    facecolor=C_CONTAINER, edgecolor="#CBD5E1", linewidth=1.0, linestyle="--")
ax.add_patch(c1)

# Card 1.1: Raw Financial Stream
r1 = FancyBboxPatch((6, 53.5), 30, 15.0, boxstyle="round,pad=0.2,rounding_size=0.5",
                    facecolor="#FFFFFF", edgecolor=THEMES[0]["bd"], linewidth=1.1)
ax.add_patch(r1)
ax.text(21, 65.5, "Financial News Stream", ha='center', va='center', fontsize=8.8, color=C_DARK, fontweight='bold')
ax.text(8, 62.0, r"$\mathrm{Target\ Entity\ (e)}:\ \mathbf{Gold}$", fontsize=7.8, color="#0369A1")
ax.text(8, 59.0, r"$\mathrm{News\ Headline\ (s)}:\ \mathbf{''Gold\ extends\ gains,\ weak\ rupee''}$", fontsize=7.2, color=C_DARK)

# Cleaner pill
cl_pill = FancyBboxPatch((7.5, 54.5), 27, 3.2, boxstyle="round,pad=0.1,rounding_size=0.3",
                         facecolor=THEMES[0]["box"], edgecolor="#BAE6FD", linewidth=0.8)
ax.add_patch(cl_pill)
ax.text(21, 56.1, "cleaner.py: Preserves $, %, loss, narrowed, dropped",
        ha='center', va='center', fontsize=6.8, color="#0284C7", fontweight='bold')

# Arrow: Stream -> Tokenizer
a1 = FancyArrowPatch((21, 53.5), (21, 48.0), arrowstyle='-|>', mutation_scale=12, color=C_MUTED, linewidth=1.4)
ax.add_patch(a1)
ax.text(22.5, 50.8, "Sentence-Pair Construction", fontsize=6.6, color=C_MUTED)

# Card 1.2: Token Sequence
r2 = FancyBboxPatch((6, 35.5), 30, 12.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                    facecolor="#FFFFFF", edgecolor=THEMES[0]["bd"], linewidth=1.1)
ax.add_patch(r2)
ax.text(21, 45.3, "Sentence-Pair Token Format", ha='center', va='center', fontsize=8.5, color=C_DARK, fontweight='bold')
ax.text(21, 41.8, r"$[\mathrm{CLS}]\ \mathbf{e}\ [\mathrm{SEP}]\ \mathbf{s}\ [\mathrm{SEP}]$",
        ha='center', va='center', fontsize=9.0, color="#0F172A", fontweight='bold')

# Shape badge
b_shape1 = FancyBboxPatch((12, 36.5), 18, 3.0, boxstyle="round,pad=0.1,rounding_size=0.3",
                          facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=0.7)
ax.add_patch(b_shape1)
ax.text(21, 38.0, r"$\mathrm{Tensor\ Shape:}\ [B, L]\quad (L = 64)$", ha='center', va='center', fontsize=7.2, color="#334155")

# Arrow: Tokenizer -> Embedding
a2 = FancyArrowPatch((21, 35.5), (21, 29.5), arrowstyle='-|>', mutation_scale=12, color=C_MUTED, linewidth=1.4)
ax.add_patch(a2)

# Card 1.3: Embedding Layer
r3 = FancyBboxPatch((6, 6.0), 30, 23.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                    facecolor=THEMES[0]["box"], edgecolor=THEMES[0]["bd"], linewidth=1.2)
ax.add_patch(r3)
ax.text(21, 27.2, "Input Embedding Stack", ha='center', va='center', fontsize=8.8, color="#0C4A6E", fontweight='bold')

embs = [
    (r"$\mathbf{E}_{\mathrm{Token}}:\ \mathrm{WordPiece\ Vocab\ (30,522)}$", 23.5),
    (r"$\mathbf{E}_{\mathrm{Segment}}:\ \mathbf{0}\ (\mathrm{Entity})\ \oplus\ \mathbf{1}\ (\mathrm{Headline})$", 19.2),
    (r"$\mathbf{E}_{\mathrm{Position}}:\ \mathrm{Learned\ Absolute\ Position}$", 15.0)
]
for lbl, y_pos in embs:
    sp = FancyBboxPatch((7.5, y_pos - 1.8), 27, 3.4, boxstyle="round,pad=0.1,rounding_size=0.3",
                        facecolor="#FFFFFF", edgecolor="#BAE6FD", linewidth=0.8)
    ax.add_patch(sp)
    ax.text(21, y_pos, lbl, ha='center', va='center', fontsize=6.8, color=C_DARK)

ax.text(21, 9.8, r"$\mathbf{H}^{(0)} = \mathbf{E}_{\mathrm{Tok}} + \mathbf{E}_{\mathrm{Seg}} + \mathbf{E}_{\mathrm{Pos}} \in \mathbb{R}^{B \times L \times 768}$",
        ha='center', va='center', fontsize=7.4, color="#0369A1", fontweight='bold')

# -------------------------------------------------------------------------
# STAGE 2: FinBERT TRANSFORMER BACKBONE (x: 42 to 84)
# -------------------------------------------------------------------------
c2 = FancyBboxPatch((42, 4), 42, 66.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                    facecolor=C_CONTAINER, edgecolor="#CBD5E1", linewidth=1.0, linestyle="--")
ax.add_patch(c2)

# Arrow from Stage 1 to Stage 2
a_s1_s2 = FancyArrowPatch((36, 9.8), (45, 9.8), arrowstyle='-|>', mutation_scale=14,
                          color=THEMES[0]["bd"], linewidth=2.0)
ax.add_patch(a_s1_s2)
ax.text(40.5, 12.0, r"$\mathbf{H}^{(0)}$", ha='center', va='center', fontsize=8.2, color=THEMES[0]["bd"], fontweight='bold')

# FinBERT Transformer Container
b_outer = FancyBboxPatch((45, 6.0), 36, 62.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                         facecolor=THEMES[1]["box"], edgecolor=THEMES[1]["bd"], linewidth=1.4)
ax.add_patch(b_outer)
ax.text(63, 66.0, "FinBERT Transformer Backbone", ha='center', va='center', fontsize=9.2, color="#78350F", fontweight='bold')
ax.text(63, 63.5, "12-Layer Pre-trained Financial Transformer Stack", ha='center', va='center', fontsize=7.0, color="#92400E", style='italic')

# Sub-block: Multi-Head Self/Cross Attention
mha_box = FancyBboxPatch((47.5, 43.0), 31, 18.0, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor=THEMES[1]["bd"], linewidth=1.0)
ax.add_patch(mha_box)
ax.text(63, 58.5, "Multi-Head Cross/Self Attention", ha='center', va='center', fontsize=8.2, color=C_DARK, fontweight='bold')
ax.text(63, 55.0, r"$\mathbf{Q} = \mathbf{H}\mathbf{W}_Q,\quad \mathbf{K} = \mathbf{H}\mathbf{W}_K,\quad \mathbf{V} = \mathbf{H}\mathbf{W}_V$",
        ha='center', va='center', fontsize=7.4, color=C_DARK)
ax.text(63, 51.0, r"$\mathrm{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d_k}}\right)\mathbf{V}$",
        ha='center', va='center', fontsize=7.6, color="#B45309", fontweight='bold')
ax.text(63, 46.8, "Cross-Attention directs Entity Q to relevant Headline K, V tokens",
        ha='center', va='center', fontsize=6.6, color="#475569", style='italic')

# Residual Connection 1
ax.annotate("", xy=(63, 43.0), xytext=(63, 37.5),
            arrowprops=dict(arrowstyle="<-", color="#B45309", lw=1.2))
ax.text(63, 40.2, "Add & Norm: LayerNorm(x + Dropout(SubLayer(x)))",
        ha='center', va='center', fontsize=6.8, color="#78350F")

# Sub-block: Feed-Forward Network
ffn_box = FancyBboxPatch((47.5, 22.5), 31, 15.0, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor=THEMES[1]["bd"], linewidth=1.0)
ax.add_patch(ffn_box)
ax.text(63, 34.8, "Position-Wise Feed-Forward Network", ha='center', va='center', fontsize=8.0, color=C_DARK, fontweight='bold')
ax.text(63, 31.0, r"$\mathrm{FFN}(\mathbf{x}) = \mathrm{GELU}(\mathbf{x}\mathbf{W}_1 + \mathbf{b}_1)\mathbf{W}_2 + \mathbf{b}_2$",
        ha='center', va='center', fontsize=7.4, color=C_DARK)
ax.text(63, 26.5, r"$d_{\mathrm{model}} = 768,\quad d_{\mathrm{ff}} = 3072,\quad N_{\mathrm{heads}} = 12$",
        ha='center', va='center', fontsize=7.2, color="#92400E", fontweight='bold')

# Repeat indicator
ax.annotate("", xy=(63, 22.5), xytext=(63, 17.0),
            arrowprops=dict(arrowstyle="<-", color="#B45309", lw=1.2))
ax.text(63, 19.5, "Repeat Stack x 12 Layers (GPU AMP fp16)",
        ha='center', va='center', fontsize=7.2, color="#78350F", fontweight='bold')

# [CLS] Output Box
cls_box = FancyBboxPatch((47.5, 7.5), 31, 8.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor="#B45309", linewidth=1.2)
ax.add_patch(cls_box)
ax.text(63, 13.5, "[CLS] Token Representation Pooling", ha='center', va='center', fontsize=8.0, color=C_DARK, fontweight='bold')
ax.text(63, 9.8, r"$\mathbf{h}_{\mathrm{CLS}} = \mathbf{H}_0^{(12)} \in \mathbb{R}^{B \times 768}$",
        ha='center', va='center', fontsize=8.4, color="#B45309", fontweight='bold')

# -------------------------------------------------------------------------
# STAGE 3: HEAD & WEIGHTED LOSS (x: 88 to 122)
# -------------------------------------------------------------------------
c3 = FancyBboxPatch((88, 4), 34, 66.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                    facecolor=C_CONTAINER, edgecolor="#CBD5E1", linewidth=1.0, linestyle="--")
ax.add_patch(c3)

# Arrow from [CLS] to Head
a_s2_s3 = FancyArrowPatch((78.5, 9.8), (91.0, 9.8), arrowstyle='-|>', mutation_scale=14,
                          color=THEMES[1]["bd"], linewidth=2.0)
ax.add_patch(a_s2_s3)
ax.text(85.0, 12.0, r"$\mathbf{h}_{\mathrm{CLS}}$", ha='center', va='center', fontsize=8.2, color=THEMES[1]["bd"], fontweight='bold')

# Linear Classifier Card
head_box = FancyBboxPatch((90.5, 6.0), 29, 21.0, boxstyle="round,pad=0.2,rounding_size=0.5",
                          facecolor=THEMES[3]["box"], edgecolor=THEMES[3]["bd"], linewidth=1.2)
ax.add_patch(head_box)
ax.text(105, 24.8, "Linear Classification Head", ha='center', va='center', fontsize=8.5, color="#14532D", fontweight='bold')
ax.text(105, 21.2, r"$\mathbf{z} = \mathbf{W}\mathbf{h}_{\mathrm{CLS}} + \mathbf{b}\quad (\mathbf{W} \in \mathbb{R}^{3 \times 768},\ \mathbf{b} \in \mathbb{R}^3)$",
        ha='center', va='center', fontsize=7.3, color=C_DARK)
ax.text(105, 17.5, r"$\hat{\mathbf{y}} = \mathrm{softmax}(\mathbf{z}) = [\hat{y}_{\mathrm{neg}}, \hat{y}_{\mathrm{neu}}, \hat{y}_{\mathrm{pos}}]^\top$",
        ha='center', va='center', fontsize=7.6, color="#15803D", fontweight='bold')
ax.text(105, 13.5, r"$\hat{y} = \arg\max_{c \in \{0, 1, 2\}}\ \mathbb{P}(Y = c \mid \mathbf{e}, \mathbf{s}; \theta)$",
        ha='center', va='center', fontsize=7.4, color="#14532D")

# Disambiguation badge
res_pill = FancyBboxPatch((92, 7.2), 26, 3.5, boxstyle="round,pad=0.1,rounding_size=0.3",
                          facecolor="#FFFFFF", edgecolor="#86EFAC", linewidth=0.8)
ax.add_patch(res_pill)
ax.text(105, 8.9, "Gold: Positive (95.5%)  |  Rupee: Negative (61.2%)",
        ha='center', va='center', fontsize=6.6, color="#166534", fontweight='bold')

# Arrow Up: Classifier -> Loss
a_head_loss = FancyArrowPatch((105, 27.0), (105, 34.0), arrowstyle='-|>', mutation_scale=12,
                              color="#15803D", linewidth=1.5)
ax.add_patch(a_head_loss)
ax.text(108.5, 30.5, r"$\hat{\mathbf{y}},\ \mathbf{y}$", fontsize=7.8, color="#15803D", fontweight='bold')

# Loss Function Card
loss_box = FancyBboxPatch((90.5, 34.5), 29, 23.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                          facecolor=THEMES[2]["box"], edgecolor=THEMES[2]["bd"], linewidth=1.3)
ax.add_patch(loss_box)
ax.text(105, 55.5, "Inverse Class Weighting (WCE)", ha='center', va='center', fontsize=8.6, color="#991B1B", fontweight='bold')

ax.text(105, 51.5, r"$\mathcal{L}_{\mathrm{WCE}} = -\sum_{c=1}^3 w_c \cdot y_c \log(\hat{y}_c)$",
        ha='center', va='center', fontsize=8.5, color="#991B1B", fontweight='bold')

ax.text(105, 47.0, r"$w_c = \frac{N}{C \times N_c}\quad (N = 3453,\ C = 3)$",
        ha='center', va='center', fontsize=7.4, color=C_DARK)

ax.text(105, 43.0, r"$w_{\mathrm{neg}} = 2.74,\quad w_{\mathrm{neu}} = 0.54,\quad w_{\mathrm{pos}} = 1.30$",
        ha='center', va='center', fontsize=7.4, color="#991B1B", fontweight='bold')

ax.text(105, 39.5, "Class ratio: Neutral 62.1%  -->  5.1x penalty on false neutrals",
        ha='center', va='center', fontsize=6.5, color="#7F1D1D", style='italic')

ax.text(105, 36.5, "Macro-F1: 89.76% (+8.47% over Linear SVM)",
        ha='center', va='center', fontsize=7.0, color="#991B1B", fontweight='bold')

# Backward Gradient Arrow
a_grad = FancyArrowPatch((90.5, 51.5), (81.0, 51.5), arrowstyle='-|>', mutation_scale=12,
                         color="#DC2626", linewidth=1.6, linestyle="--")
ax.add_patch(a_grad)
ax.text(85.5, 53.5, r"$\nabla_\theta \mathcal{L}_{\mathrm{WCE}}$", ha='center', va='center', fontsize=7.8, color="#DC2626", fontweight='bold')

# Statistical Test Badge
stat_box = FancyBboxPatch((90.5, 59.5), 29, 9.0, boxstyle="round,pad=0.2,rounding_size=0.5",
                          facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1.0)
ax.add_patch(stat_box)
ax.text(105, 66.0, "McNemar Statistical Significance", ha='center', va='center', fontsize=7.8, color=C_DARK, fontweight='bold')
ax.text(105, 63.0, r"$\chi^2 = 9.47,\quad p = 0.0021 < 0.01$", ha='center', va='center', fontsize=7.6, color="#1E293B", fontweight='bold')
ax.text(105, 61.0, "Statistically significant improvement over Linear SVM",
        ha='center', va='center', fontsize=6.2, color="#64748B", style='italic')

# -------------------------------------------------------------------------
# STAGE 4: PRODUCTION DEPLOYMENT & CLIENT ECOSYSTEM (x: 126 to 156)
# -------------------------------------------------------------------------
c4 = FancyBboxPatch((126, 4), 30, 66.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                    facecolor=C_CONTAINER, edgecolor="#CBD5E1", linewidth=1.0, linestyle="--")
ax.add_patch(c4)

# Arrow from Classifier to API
a_s3_s4 = FancyArrowPatch((119.5, 16.5), (128.5, 16.5), arrowstyle='-|>', mutation_scale=14,
                          color=THEMES[3]["bd"], linewidth=2.0)
ax.add_patch(a_s3_s4)
ax.text(124.0, 19.0, r"$\hat{\mathbf{y}}$", ha='center', va='center', fontsize=8.2, color=THEMES[3]["bd"], fontweight='bold')

# FastAPI Engine Card
api_box = FancyBboxPatch((128.5, 6.0), 25, 25.0, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor=THEMES[3]["bd"], linewidth=1.2)
ax.add_patch(api_box)
ax.text(141, 28.5, "FastAPI ASGI Engine", ha='center', va='center', fontsize=8.6, color="#14532D", fontweight='bold')
ax.text(141, 25.8, "PyTorch CUDA (AMP fp16 Kernel)", ha='center', va='center', fontsize=6.8, color="#166534")

ax.text(130, 22.5, "POST /predict/sentiment", fontsize=6.8, color=C_DARK, fontweight='bold')
ax.text(130, 19.8, "Sentence-level (PhraseBank)", fontsize=6.2, color="#64748B")
ax.text(130, 16.8, "POST /predict/entity-sentiment", fontsize=6.8, color=C_DARK, fontweight='bold')
ax.text(130, 14.0, "Entity-aware (SEntFiN 1.0)", fontsize=6.2, color="#64748B")

# Latency badge
lat_pill = FancyBboxPatch((130, 8.0), 22, 4.0, boxstyle="round,pad=0.1,rounding_size=0.3",
                          facecolor="#F0FDF4", edgecolor="#86EFAC", linewidth=0.8)
ax.add_patch(lat_pill)
ax.text(141, 10.0, "Latency: 18.2 ms (p95 on RTX 3050)",
        ha='center', va='center', fontsize=6.8, color="#15803D", fontweight='bold')

# Bi-directional Arrow: API <-> UI
a_api_ui = FancyArrowPatch((141, 31.0), (141, 37.5), arrowstyle='<|-|>', mutation_scale=12,
                           color=THEMES[3]["bd"], linewidth=1.5)
ax.add_patch(a_api_ui)
ax.text(145.5, 34.2, "REST JSON", fontsize=6.6, color=THEMES[3]["bd"], fontweight='bold')

# Client Ecosystem Outer Card
ui_card = FancyBboxPatch((128.5, 38.5), 25, 30.0, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor=THEMES[0]["bd"], linewidth=1.2)
ax.add_patch(ui_card)
ax.text(141, 66.0, "Client Applications", ha='center', va='center', fontsize=8.6, color="#0369A1", fontweight='bold')

# Sub-client 1: React Web Terminal
ui_react = FancyBboxPatch((130, 53.0), 22, 11.0, boxstyle="round,pad=0.1,rounding_size=0.3",
                          facecolor=THEMES[0]["box"], edgecolor="#7DD3FC", linewidth=0.8)
ax.add_patch(ui_react)
ax.text(141, 61.5, "React Terminal 2.0", ha='center', va='center', fontsize=7.8, color="#0C4A6E", fontweight='bold')
ax.text(141, 58.5, "Dual-mode Sandbox UI", ha='center', va='center', fontsize=6.5, color=C_DARK)
ax.text(141, 55.5, "Real-time Probability Gauges", ha='center', va='center', fontsize=6.2, color="#64748B")

# Sub-client 2: Chrome Extension V3
ui_ext = FancyBboxPatch((130, 40.5), 22, 11.0, boxstyle="round,pad=0.1,rounding_size=0.3",
                        facecolor=THEMES[3]["box"], edgecolor="#86EFAC", linewidth=0.8)
ax.add_patch(ui_ext)
ax.text(141, 49.0, "Chrome Extension V3", ha='center', va='center', fontsize=7.8, color="#14532D", fontweight='bold')
ax.text(141, 46.0, "Browser In-situ Highlighting", ha='center', va='center', fontsize=6.5, color=C_DARK)
ax.text(141, 43.0, "Entity Disambiguation Routing", ha='center', va='center', fontsize=6.2, color="#64748B")

# Output paths
out_dir = r"d:\Vscode-luyện code\Financial Sentiment Tracker (FinBERT Powered)\docs"
os.makedirs(out_dir, exist_ok=True)
png_path = os.path.join(out_dir, "academic_system_architecture.png")
pdf_path = os.path.join(out_dir, "academic_system_architecture.pdf")

gdrive_dir = r"G:\My Drive\Study\FPT University AI\Kì 5\Text Mining (TMG301)\Project"
gdrive_png = os.path.join(gdrive_dir, "academic_system_architecture.png")
gdrive_pdf = os.path.join(gdrive_dir, "academic_system_architecture.pdf")

plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
plt.savefig(pdf_path, bbox_inches='tight', facecolor='#FFFFFF')
if os.path.exists(gdrive_dir):
    plt.savefig(gdrive_png, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.savefig(gdrive_pdf, bbox_inches='tight', facecolor='#FFFFFF')

print("SUCCESS! Publication architecture diagram generated:")
print("PNG:", png_path)
print("PDF:", pdf_path)
if os.path.exists(gdrive_dir):
    print("Google Drive PNG:", gdrive_png)
