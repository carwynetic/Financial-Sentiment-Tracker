import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# 1. Strictly Configure Arial Font and Mathtext
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'mathtext.fontset': 'stixsans',  # Clean sans-serif math font matching Arial
    'figure.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42
})

# Generous 16:9 widescreen canvas
fig, ax = plt.subplots(figsize=(18.5, 9.8), dpi=300)
ax.set_xlim(0, 182)
ax.set_ylim(0, 94)
ax.axis('off')

# Professional Academic Color Palette (Nature / NeurIPS camera-ready style)
C_DARK = "#0F172A"       # Primary text
C_MUTED = "#334155"      # Secondary text
C_LIGHT_MUTED = "#64748B"# Tertiary text / caption
C_CONTAINER_BG = "#F8FAFC"
C_CONTAINER_BD = "#CBD5E1"

# Stage-specific subtle fills and crisp borders
THEMES = [
    {"fill": "#FFFFFF", "bd": "#0284C7", "txt": "#0369A1", "hdr": "#E0F2FE", "box": "#F0F9FF"},  # Stage 1: Sky
    {"fill": "#FFFFFF", "bd": "#D97706", "txt": "#B45309", "hdr": "#FEF3C7", "box": "#FFFBEB"},  # Stage 2: Amber
    {"fill": "#FFFFFF", "bd": "#DC2626", "txt": "#B91C1C", "hdr": "#FEE2E2", "box": "#FEF2F2"},  # Stage 3: Rose
    {"fill": "#FFFFFF", "bd": "#16A34A", "txt": "#15803D", "hdr": "#DCFCE7", "box": "#F0FDF4"}   # Stage 4: Green
]

# Helper function to guarantee text NEVER overflows any card boundary
def fit_text(x, y, s, card_x, card_w, ha="center", va="center", fontsize=8.2, min_fontsize=5.2, margin=1.2, **kwargs):
    t = ax.text(x, y, s, ha=ha, va=va, fontsize=fontsize, fontfamily='Arial', **kwargs)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    bbox = t.get_window_extent(renderer).transformed(inv)
    
    curr_size = fontsize
    while (bbox.x0 < card_x + margin or bbox.x1 > card_x + card_w - margin) and curr_size > min_fontsize:
        curr_size -= 0.3
        t.set_fontsize(curr_size)
        fig.canvas.draw()
        bbox = t.get_window_extent(renderer).transformed(inv)
        
    return t

# -------------------------------------------------------------------------
# 0. MAIN HEADER (Clean Academic Layout)
# -------------------------------------------------------------------------
ax.text(91, 91.0, "Figure 1: End-to-End System Architecture for Entity-Aware Financial Sentiment Analysis",
        ha='center', va='center', fontsize=14.0, color=C_DARK, fontweight='bold', fontfamily='Arial')
ax.text(91, 88.2, "Raw Financial Stream  -->  Sentence-Pair Cross-Attention  -->  FinBERT Encoder  -->  Cost-Sensitive WCE Loss  -->  Production Inference",
        ha='center', va='center', fontsize=9.0, color=C_MUTED, style='italic', fontfamily='Arial')

# Top Stage Banners
stage_headers = [
    (4, 43, "Stage 1: Input & Embedding", "Financial Cleaner & Tokenizer", THEMES[0]),
    (48, 96, "Stage 2: Domain FinBERT Backbone", "12-Layer Transformer Encoder", THEMES[1]),
    (101, 140, "Stage 3: Head & Cost-Sensitive Loss", "Multi-Entity Disambiguation & WCE", THEMES[2]),
    (145, 178, "Stage 4: Production Deployment", "FastAPI & Client Applications", THEMES[3])
]

for x1, x2, t1, t2, th in stage_headers:
    w = x2 - x1
    p = FancyBboxPatch((x1, 79.5), w, 5.0, boxstyle="round,pad=0.2,rounding_size=0.6",
                       facecolor=th["hdr"], edgecolor=th["bd"], linewidth=1.3)
    ax.add_patch(p)
    ax.text(x1 + w/2, 82.8, t1, ha='center', va='center', fontsize=9.0, color=th["txt"], fontweight='bold', fontfamily='Arial')
    ax.text(x1 + w/2, 81.0, t2, ha='center', va='center', fontsize=7.2, color=C_MUTED, style='italic', fontfamily='Arial')

# -------------------------------------------------------------------------
# STAGE 1: INPUT REPRESENTATION & EMBEDDINGS (x: 4 to 43, width 39)
# -------------------------------------------------------------------------
s1_x, s1_w = 4, 39
c1 = FancyBboxPatch((s1_x, 4), s1_w, 73.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                    facecolor=C_CONTAINER_BG, edgecolor=C_CONTAINER_BD, linewidth=1.0, linestyle="--")
ax.add_patch(c1)

# Card 1.1: Raw Financial Stream
r1_x, r1_y, r1_w, r1_h = 6.5, 59.0, 34.0, 16.0
r1 = FancyBboxPatch((r1_x, r1_y), r1_w, r1_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                    facecolor="#FFFFFF", edgecolor=THEMES[0]["bd"], linewidth=1.1)
ax.add_patch(r1)
fit_text(r1_x + r1_w/2, r1_y + 13.5, "Financial News Stream", r1_x, r1_w, fontsize=9.2, color=C_DARK, fontweight='bold')
fit_text(r1_x + 2.0, r1_y + 10.0, r"$\mathrm{Target\ Entity\ (e)}:\ \mathbf{Gold}$", r1_x, r1_w, ha='left', fontsize=8.0, color="#0369A1")
fit_text(r1_x + 2.0, r1_y + 6.8, r"$\mathrm{Headline\ (s)}:\ \mathbf{''Gold\ extends\ gains,\ weak\ rupee''}$", r1_x, r1_w, ha='left', fontsize=7.2, color=C_DARK)

# Cleaner pill
cl_x, cl_y, cl_w, cl_h = 8.0, 60.0, 31.0, 3.5
cl_pill = FancyBboxPatch((cl_x, cl_y), cl_w, cl_h, boxstyle="round,pad=0.1,rounding_size=0.3",
                         facecolor=THEMES[0]["box"], edgecolor="#BAE6FD", linewidth=0.8)
ax.add_patch(cl_pill)
fit_text(cl_x + cl_w/2, cl_y + cl_h/2, "cleaner.py: Preserves $, %, loss, narrowed", cl_x, cl_w, fontsize=7.0, color="#0284C7", fontweight='bold')

# Arrow: Stream -> Tokenizer
a1 = FancyArrowPatch((r1_x + r1_w/2, r1_y), (r1_x + r1_w/2, 53.0), arrowstyle='-|>', mutation_scale=12, color=C_MUTED, linewidth=1.4)
ax.add_patch(a1)
fit_text(r1_x + r1_w/2 + 7.5, 56.0, "Sentence-Pair", r1_x, r1_w, fontsize=6.8, color=C_MUTED)

# Card 1.2: Token Sequence
r2_x, r2_y, r2_w, r2_h = 6.5, 38.5, 34.0, 14.5
r2 = FancyBboxPatch((r2_x, r2_y), r2_w, r2_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                    facecolor="#FFFFFF", edgecolor=THEMES[0]["bd"], linewidth=1.1)
ax.add_patch(r2)
fit_text(r2_x + r2_w/2, r2_y + 11.5, "Sentence-Pair Token Format", r2_x, r2_w, fontsize=9.0, color=C_DARK, fontweight='bold')
fit_text(r2_x + r2_w/2, r2_y + 7.5, r"$[\mathrm{CLS}]\ \mathbf{e}\ [\mathrm{SEP}]\ \mathbf{s}\ [\mathrm{SEP}]$", r2_x, r2_w, fontsize=9.5, color="#0F172A", fontweight='bold')

# Shape badge
b_shape1 = FancyBboxPatch((r2_x + 6.0, r2_y + 2.0), 22.0, 3.2, boxstyle="round,pad=0.1,rounding_size=0.3",
                          facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=0.7)
ax.add_patch(b_shape1)
fit_text(r2_x + r2_w/2, r2_y + 3.6, r"$\mathrm{Tensor\ Shape:}\ [B, L]\quad (L = 64)$", r2_x, r2_w, fontsize=7.4, color="#334155")

# Arrow: Tokenizer -> Embedding
a2 = FancyArrowPatch((r2_x + r2_w/2, r2_y), (r2_x + r2_w/2, 31.5), arrowstyle='-|>', mutation_scale=12, color=C_MUTED, linewidth=1.4)
ax.add_patch(a2)

# Card 1.3: Embedding Layer
r3_x, r3_y, r3_w, r3_h = 6.5, 6.0, 34.0, 25.5
r3 = FancyBboxPatch((r3_x, r3_y), r3_w, r3_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                    facecolor=THEMES[0]["box"], edgecolor=THEMES[0]["bd"], linewidth=1.2)
ax.add_patch(r3)
fit_text(r3_x + r3_w/2, r3_y + 22.8, "Input Embedding Stack", r3_x, r3_w, fontsize=9.2, color="#0C4A6E", fontweight='bold')

embs = [
    (r"$\mathbf{E}_{\mathrm{Token}}:\ \mathrm{WordPiece\ Vocab\ (30,522)}$", r3_y + 18.2),
    (r"$\mathbf{E}_{\mathrm{Segment}}:\ \mathbf{0}\ (\mathrm{Entity})\ \oplus\ \mathbf{1}\ (\mathrm{Headline})$", r3_y + 13.5),
    (r"$\mathbf{E}_{\mathrm{Position}}:\ \mathrm{Learned\ Absolute\ Position}$", r3_y + 8.8)
]
for lbl, y_pos in embs:
    sp = FancyBboxPatch((r3_x + 2.0, y_pos - 1.8), r3_w - 4.0, 3.6, boxstyle="round,pad=0.1,rounding_size=0.3",
                        facecolor="#FFFFFF", edgecolor="#BAE6FD", linewidth=0.8)
    ax.add_patch(sp)
    fit_text(r3_x + r3_w/2, y_pos, lbl, r3_x + 2.0, r3_w - 4.0, fontsize=7.2, color=C_DARK)

fit_text(r3_x + r3_w/2, r3_y + 3.0, r"$\mathbf{H}^{(0)} = \mathbf{E}_{\mathrm{Tok}} + \mathbf{E}_{\mathrm{Seg}} + \mathbf{E}_{\mathrm{Pos}} \in \mathbb{R}^{B \times L \times 768}$",
         r3_x, r3_w, fontsize=7.6, color="#0369A1", fontweight='bold')

# -------------------------------------------------------------------------
# STAGE 2: FinBERT TRANSFORMER BACKBONE (x: 48 to 96, width 48)
# -------------------------------------------------------------------------
s2_x, s2_w = 48, 48
c2 = FancyBboxPatch((s2_x, 4), s2_w, 73.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                    facecolor=C_CONTAINER_BG, edgecolor=C_CONTAINER_BD, linewidth=1.0, linestyle="--")
ax.add_patch(c2)

# Horizontal Arrow from Stage 1 to Stage 2
a_s1_s2 = FancyArrowPatch((r3_x + r3_w, r3_y + 3.0), (s2_x + 3.0, r3_y + 3.0), arrowstyle='-|>', mutation_scale=14,
                          color=THEMES[0]["bd"], linewidth=2.0)
ax.add_patch(a_s1_s2)
fit_text((r3_x + r3_w + s2_x + 3.0)/2, r3_y + 5.5, r"$\mathbf{H}^{(0)}$", r3_x + r3_w, s2_x - r3_x - r3_w + 6.0, fontsize=8.4, color=THEMES[0]["bd"], fontweight='bold')

# FinBERT Transformer Container
b_outer_x, b_outer_y, b_outer_w, b_outer_h = s2_x + 3.0, 6.0, s2_w - 6.0, 69.0
b_outer = FancyBboxPatch((b_outer_x, b_outer_y), b_outer_w, b_outer_h, boxstyle="round,pad=0.3,rounding_size=0.8",
                         facecolor=THEMES[1]["box"], edgecolor=THEMES[1]["bd"], linewidth=1.4)
ax.add_patch(b_outer)
fit_text(b_outer_x + b_outer_w/2, b_outer_y + 65.5, "FinBERT Transformer Backbone", b_outer_x, b_outer_w, fontsize=9.8, color="#78350F", fontweight='bold')
fit_text(b_outer_x + b_outer_w/2, b_outer_y + 62.8, "12-Layer Pre-trained Financial Transformer Stack", b_outer_x, b_outer_w, fontsize=7.4, color="#92400E", style='italic')

# Sub-block: Multi-Head Self/Cross Attention
mha_x, mha_y, mha_w, mha_h = b_outer_x + 2.5, 43.5, b_outer_w - 5.0, 18.0
mha_box = FancyBboxPatch((mha_x, mha_y), mha_w, mha_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor=THEMES[1]["bd"], linewidth=1.0)
ax.add_patch(mha_box)
fit_text(mha_x + mha_w/2, mha_y + 14.5, "Multi-Head Cross/Self Attention", mha_x, mha_w, fontsize=8.6, color=C_DARK, fontweight='bold')
fit_text(mha_x + mha_w/2, mha_y + 11.0, r"$\mathbf{Q} = \mathbf{H}\mathbf{W}_Q,\quad \mathbf{K} = \mathbf{H}\mathbf{W}_K,\quad \mathbf{V} = \mathbf{H}\mathbf{W}_V$", mha_x, mha_w, fontsize=7.8, color=C_DARK)
fit_text(mha_x + mha_w/2, mha_y + 7.0, r"$\mathrm{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d_k}}\right)\mathbf{V}$", mha_x, mha_w, fontsize=8.0, color="#B45309", fontweight='bold')
fit_text(mha_x + mha_w/2, mha_y + 3.2, "Cross-Attention directs Entity Q to relevant Headline K, V tokens", mha_x, mha_w, fontsize=7.0, color="#475569", style='italic')

# Residual Connection 1
ax.annotate("", xy=(b_outer_x + b_outer_w/2, mha_y), xytext=(b_outer_x + b_outer_w/2, 38.0),
            arrowprops=dict(arrowstyle="<-", color="#B45309", lw=1.2))
fit_text(b_outer_x + b_outer_w/2, 40.8, "Add & Norm: LayerNorm(x + Dropout(SubLayer(x)))", b_outer_x, b_outer_w, fontsize=7.2, color="#78350F")

# Sub-block: Feed-Forward Network
ffn_x, ffn_y, ffn_w, ffn_h = b_outer_x + 2.5, 23.0, b_outer_w - 5.0, 15.0
ffn_box = FancyBboxPatch((ffn_x, ffn_y), ffn_w, ffn_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor=THEMES[1]["bd"], linewidth=1.0)
ax.add_patch(ffn_box)
fit_text(ffn_x + ffn_w/2, ffn_y + 11.8, "Position-Wise Feed-Forward Network", ffn_x, ffn_w, fontsize=8.4, color=C_DARK, fontweight='bold')
fit_text(ffn_x + ffn_w/2, ffn_y + 7.8, r"$\mathrm{FFN}(\mathbf{x}) = \mathrm{GELU}(\mathbf{x}\mathbf{W}_1 + \mathbf{b}_1)\mathbf{W}_2 + \mathbf{b}_2$", ffn_x, ffn_w, fontsize=7.8, color=C_DARK)
fit_text(ffn_x + ffn_w/2, ffn_y + 3.8, r"$d_{\mathrm{model}} = 768,\quad d_{\mathrm{ff}} = 3072,\quad N_{\mathrm{heads}} = 12$", ffn_x, ffn_w, fontsize=7.4, color="#92400E", fontweight='bold')

# Repeat indicator
ax.annotate("", xy=(b_outer_x + b_outer_w/2, ffn_y), xytext=(b_outer_x + b_outer_w/2, 17.5),
            arrowprops=dict(arrowstyle="<-", color="#B45309", lw=1.2))
fit_text(b_outer_x + b_outer_w/2, 20.2, "Repeat Stack x 12 Layers (GPU AMP fp16)", b_outer_x, b_outer_w, fontsize=7.4, color="#78350F", fontweight='bold')

# [CLS] Output Box
cls_x, cls_y, cls_w, cls_h = b_outer_x + 2.5, 7.5, b_outer_w - 5.0, 9.5
cls_box = FancyBboxPatch((cls_x, cls_y), cls_w, cls_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor="#B45309", linewidth=1.2)
ax.add_patch(cls_box)
fit_text(cls_x + cls_w/2, cls_y + 6.8, "[CLS] Token Representation Pooling", cls_x, cls_w, fontsize=8.4, color=C_DARK, fontweight='bold')
fit_text(cls_x + cls_w/2, cls_y + 2.8, r"$\mathbf{h}_{\mathrm{CLS}} = \mathbf{H}_0^{(12)} \in \mathbb{R}^{B \times 768}$", cls_x, cls_w, fontsize=8.8, color="#B45309", fontweight='bold')

# -------------------------------------------------------------------------
# STAGE 3: HEAD & WEIGHTED LOSS (x: 101 to 140, width 39)
# -------------------------------------------------------------------------
s3_x, s3_w = 101, 39
c3 = FancyBboxPatch((s3_x, 4), s3_w, 73.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                    facecolor=C_CONTAINER_BG, edgecolor=C_CONTAINER_BD, linewidth=1.0, linestyle="--")
ax.add_patch(c3)

# Arrow from [CLS] to Head
a_s2_s3 = FancyArrowPatch((cls_x + cls_w, cls_y + 4.5), (s3_x + 2.5, cls_y + 4.5), arrowstyle='-|>', mutation_scale=14,
                          color=THEMES[1]["bd"], linewidth=2.0)
ax.add_patch(a_s2_s3)
fit_text((cls_x + cls_w + s3_x + 2.5)/2, cls_y + 7.0, r"$\mathbf{h}_{\mathrm{CLS}}$", cls_x + cls_w, s3_x - cls_x - cls_w + 5.0, fontsize=8.4, color=THEMES[1]["bd"], fontweight='bold')

# Linear Classifier Card
head_x, head_y, head_w, head_h = s3_x + 2.5, 6.0, s3_w - 5.0, 23.0
head_box = FancyBboxPatch((head_x, head_y), head_w, head_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                          facecolor=THEMES[3]["box"], edgecolor=THEMES[3]["bd"], linewidth=1.2)
ax.add_patch(head_box)
fit_text(head_x + head_w/2, head_y + 19.5, "Linear Classification Head", head_x, head_w, fontsize=8.8, color="#14532D", fontweight='bold')
fit_text(head_x + head_w/2, head_y + 15.5, r"$\mathbf{z} = \mathbf{W}\mathbf{h}_{\mathrm{CLS}} + \mathbf{b}\quad (\mathbf{W} \in \mathbb{R}^{3 \times 768},\ \mathbf{b} \in \mathbb{R}^3)$", head_x, head_w, fontsize=7.6, color=C_DARK)
fit_text(head_x + head_w/2, head_y + 11.5, r"$\hat{\mathbf{y}} = \mathrm{softmax}(\mathbf{z}) = [\hat{y}_{\mathrm{neg}}, \hat{y}_{\mathrm{neu}}, \hat{y}_{\mathrm{pos}}]^\top$", head_x, head_w, fontsize=7.8, color="#15803D", fontweight='bold')
fit_text(head_x + head_w/2, head_y + 7.5, r"$\hat{y} = \arg\max_{c \in \{0, 1, 2\}}\ \mathbb{P}(Y = c \mid \mathbf{e}, \mathbf{s}; \theta)$", head_x, head_w, fontsize=7.6, color="#14532D")

# Disambiguation badge
res_pill = FancyBboxPatch((head_x + 2.0, head_y + 1.8), head_w - 4.0, 3.8, boxstyle="round,pad=0.1,rounding_size=0.3",
                          facecolor="#FFFFFF", edgecolor="#86EFAC", linewidth=0.8)
ax.add_patch(res_pill)
fit_text(head_x + head_w/2, head_y + 3.7, "Gold: Positive (95.5%)  |  Rupee: Negative (61.2%)", head_x + 2.0, head_w - 4.0, fontsize=6.8, color="#166534", fontweight='bold')

# Arrow Up: Classifier -> Loss
a_head_loss = FancyArrowPatch((head_x + head_w/2, head_y + head_h), (head_x + head_w/2, 36.5), arrowstyle='-|>', mutation_scale=12,
                              color="#15803D", linewidth=1.5)
ax.add_patch(a_head_loss)
fit_text(head_x + head_w/2 + 5.0, 33.0, r"$\hat{\mathbf{y}},\ \mathbf{y}$", head_x, head_w, fontsize=8.0, color="#15803D", fontweight='bold')

# Loss Function Card
loss_x, loss_y, loss_w, loss_h = s3_x + 2.5, 37.0, s3_w - 5.0, 24.5
loss_box = FancyBboxPatch((loss_x, loss_y), loss_w, loss_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                          facecolor=THEMES[2]["box"], edgecolor=THEMES[2]["bd"], linewidth=1.3)
ax.add_patch(loss_box)
fit_text(loss_x + loss_w/2, loss_y + 21.0, "Inverse Class Weighting (WCE)", loss_x, loss_w, fontsize=8.8, color="#991B1B", fontweight='bold')
fit_text(loss_x + loss_w/2, loss_y + 16.5, r"$\mathcal{L}_{\mathrm{WCE}} = -\sum_{c=1}^3 w_c \cdot y_c \log(\hat{y}_c)$", loss_x, loss_w, fontsize=8.8, color="#991B1B", fontweight='bold')
fit_text(loss_x + loss_w/2, loss_y + 12.5, r"$w_c = \frac{N}{C \times N_c}\quad (N = 3453,\ C = 3)$", loss_x, loss_w, fontsize=7.6, color=C_DARK)
fit_text(loss_x + loss_w/2, loss_y + 8.5, r"$w_{\mathrm{neg}} = 2.74,\quad w_{\mathrm{neu}} = 0.54,\quad w_{\mathrm{pos}} = 1.30$", loss_x, loss_w, fontsize=7.6, color="#991B1B", fontweight='bold')
fit_text(loss_x + loss_w/2, loss_y + 4.8, "Neutral ratio: 62.1%  -->  5.1x penalty on false neutrals", loss_x, loss_w, fontsize=6.8, color="#7F1D1D", style='italic')
fit_text(loss_x + loss_w/2, loss_y + 1.8, "Macro-F1: 89.76% (+8.47% over Linear SVM)", loss_x, loss_w, fontsize=7.2, color="#991B1B", fontweight='bold')

# Backward Gradient Arrow
a_grad = FancyArrowPatch((loss_x, loss_y + 16.5), (s2_x + s2_w - 3.0, loss_y + 16.5), arrowstyle='-|>', mutation_scale=12,
                         color="#DC2626", linewidth=1.6, linestyle="--")
ax.add_patch(a_grad)
fit_text((loss_x + s2_x + s2_w - 3.0)/2, loss_y + 18.8, r"$\nabla_\theta \mathcal{L}_{\mathrm{WCE}}$", s2_x + s2_w - 3.0, loss_x - (s2_x + s2_w - 3.0), fontsize=8.0, color="#DC2626", fontweight='bold')

# Statistical Test Badge
stat_x, stat_y, stat_w, stat_h = s3_x + 2.5, 63.0, s3_w - 5.0, 9.5
stat_box = FancyBboxPatch((stat_x, stat_y), stat_w, stat_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                          facecolor="#FFFFFF", edgecolor="#94A3B8", linewidth=1.0)
ax.add_patch(stat_box)
fit_text(stat_x + stat_w/2, stat_y + 6.8, "McNemar Statistical Significance", stat_x, stat_w, fontsize=8.0, color=C_DARK, fontweight='bold')
fit_text(stat_x + stat_w/2, stat_y + 3.8, r"$\chi^2 = 9.47,\quad p = 0.0021 < 0.01$", stat_x, stat_w, fontsize=7.8, color="#1E293B", fontweight='bold')
fit_text(stat_x + stat_w/2, stat_y + 1.5, "Statistically significant improvement over Linear SVM", stat_x, stat_w, fontsize=6.4, color="#64748B", style='italic')

# -------------------------------------------------------------------------
# STAGE 4: PRODUCTION DEPLOYMENT & CLIENT ECOSYSTEM (x: 145 to 178, width 33)
# -------------------------------------------------------------------------
s4_x, s4_w = 145, 33
c4 = FancyBboxPatch((s4_x, 4), s4_w, 73.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                    facecolor=C_CONTAINER_BG, edgecolor=C_CONTAINER_BD, linewidth=1.0, linestyle="--")
ax.add_patch(c4)

# Arrow from Classifier to API
a_s3_s4 = FancyArrowPatch((head_x + head_w, head_y + 11.5), (s4_x + 2.5, head_y + 11.5), arrowstyle='-|>', mutation_scale=14,
                          color=THEMES[3]["bd"], linewidth=2.0)
ax.add_patch(a_s3_s4)
fit_text((head_x + head_w + s4_x + 2.5)/2, head_y + 14.0, r"$\hat{\mathbf{y}}$", head_x + head_w, s4_x - head_x - head_w + 5.0, fontsize=8.4, color=THEMES[3]["bd"], fontweight='bold')

# FastAPI Engine Card
api_x, api_y, api_w, api_h = s4_x + 2.5, 6.0, s4_w - 5.0, 26.0
api_box = FancyBboxPatch((api_x, api_y), api_w, api_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor=THEMES[3]["bd"], linewidth=1.2)
ax.add_patch(api_box)
fit_text(api_x + api_w/2, api_y + 22.5, "FastAPI ASGI Engine", api_x, api_w, fontsize=8.8, color="#14532D", fontweight='bold')
fit_text(api_x + api_w/2, api_y + 19.5, "PyTorch CUDA (AMP fp16 Kernel)", api_x, api_w, fontsize=7.0, color="#166534")

fit_text(api_x + 2.0, api_y + 16.0, "POST /predict/sentiment", api_x, api_w, ha='left', fontsize=6.8, color=C_DARK, fontweight='bold')
fit_text(api_x + 3.5, api_y + 13.5, "Sentence-level (PhraseBank)", api_x, api_w, ha='left', fontsize=6.2, color="#64748B")
fit_text(api_x + 2.0, api_y + 10.5, "POST /predict/entity-sentiment", api_x, api_w, ha='left', fontsize=6.8, color=C_DARK, fontweight='bold')
fit_text(api_x + 3.5, api_y + 8.0, "Entity-aware (SEntFiN 1.0)", api_x, api_w, ha='left', fontsize=6.2, color="#64748B")

# Latency badge
lat_pill = FancyBboxPatch((api_x + 2.0, api_y + 1.8), api_w - 4.0, 4.2, boxstyle="round,pad=0.1,rounding_size=0.3",
                          facecolor="#F0FDF4", edgecolor="#86EFAC", linewidth=0.8)
ax.add_patch(lat_pill)
fit_text(api_x + api_w/2, api_y + 3.9, "Latency: 18.2 ms (p95 on RTX 3050)", api_x + 2.0, api_w - 4.0, fontsize=7.0, color="#15803D", fontweight='bold')

# Bi-directional Arrow: API <-> UI
a_api_ui = FancyArrowPatch((api_x + api_w/2, api_y + api_h), (api_x + api_w/2, 38.0), arrowstyle='<|-|>', mutation_scale=12,
                           color=THEMES[3]["bd"], linewidth=1.5)
ax.add_patch(a_api_ui)
fit_text(api_x + api_w/2 + 6.0, 35.0, "REST JSON", api_x, api_w, fontsize=6.8, color=THEMES[3]["bd"], fontweight='bold')

# Client Ecosystem Outer Card
ui_x, ui_y, ui_w, ui_h = s4_x + 2.5, 39.0, s4_w - 5.0, 33.5
ui_card = FancyBboxPatch((ui_x, ui_y), ui_w, ui_h, boxstyle="round,pad=0.2,rounding_size=0.5",
                         facecolor="#FFFFFF", edgecolor=THEMES[0]["bd"], linewidth=1.2)
ax.add_patch(ui_card)
fit_text(ui_x + ui_w/2, ui_y + 30.0, "Client Applications", ui_x, ui_w, fontsize=8.8, color="#0369A1", fontweight='bold')

# Sub-client 1: React Web Terminal
r_term_x, r_term_y, r_term_w, r_term_h = ui_x + 2.0, ui_y + 15.5, ui_w - 4.0, 12.5
ui_react = FancyBboxPatch((r_term_x, r_term_y), r_term_w, r_term_h, boxstyle="round,pad=0.1,rounding_size=0.3",
                          facecolor=THEMES[0]["box"], edgecolor="#7DD3FC", linewidth=0.8)
ax.add_patch(ui_react)
fit_text(r_term_x + r_term_w/2, r_term_y + 9.5, "React Terminal 2.0", r_term_x, r_term_w, fontsize=8.0, color="#0C4A6E", fontweight='bold')
fit_text(r_term_x + r_term_w/2, r_term_y + 6.2, "Dual-mode Sandbox UI", r_term_x, r_term_w, fontsize=6.8, color=C_DARK)
fit_text(r_term_x + r_term_w/2, r_term_y + 3.0, "Real-time Probability Gauges", r_term_x, r_term_w, fontsize=6.4, color="#64748B")

# Sub-client 2: Chrome Extension V3
ext_x, ext_y, ext_w, ext_h = ui_x + 2.0, ui_y + 1.8, ui_w - 4.0, 12.5
ui_ext = FancyBboxPatch((ext_x, ext_y), ext_w, ext_h, boxstyle="round,pad=0.1,rounding_size=0.3",
                        facecolor=THEMES[3]["box"], edgecolor="#86EFAC", linewidth=0.8)
ax.add_patch(ui_ext)
fit_text(ext_x + ext_w/2, ext_y + 9.5, "Chrome Extension V3", ext_x, ext_w, fontsize=8.0, color="#14532D", fontweight='bold')
fit_text(ext_x + ext_w/2, ext_y + 6.2, "Browser In-situ Highlighting", ext_x, ext_w, fontsize=6.8, color=C_DARK)
fit_text(ext_x + ext_w/2, ext_y + 3.0, "Entity Disambiguation Routing", ext_x, ext_w, fontsize=6.4, color="#64748B")

# -------------------------------------------------------------------------
# OUTPUT EXPORTS
# -------------------------------------------------------------------------
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

print("SUCCESS! Arial-fitted diagram generated successfully:")
print("PNG:", png_path)
print("PDF:", pdf_path)
if os.path.exists(gdrive_dir):
    print("Google Drive PNG:", gdrive_png)
