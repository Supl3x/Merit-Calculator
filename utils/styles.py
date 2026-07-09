# ── Merit Calculator — Custom CSS & Theme ─────────────────────────────────────
"""
Inject premium dark-glassmorphism CSS into Streamlit.
"""

GOOGLE_FONT_IMPORT = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
</style>
"""

MAIN_CSS = """
<style>
/* ── Global ────────────────────────────────────────────────────── */
:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: rgba(17, 24, 39, 0.7);
    --border-subtle: rgba(255, 255, 255, 0.06);
    --text-primary: #f9fafb;
    --text-secondary: #9ca3af;
    --accent-indigo: #6C63FF;
    --accent-emerald: #10B981;
    --accent-amber: #F59E0B;
    --accent-rose: #EF4444;
    --accent-purple: #8B5CF6;
    --glass-bg: rgba(255, 255, 255, 0.03);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

html, body, [class*="st-"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: var(--bg-primary) !important;
}

/* ── Sidebar ───────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1629 0%, #1a1040 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
}

section[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    transition: all 0.3s ease !important;
    padding: 8px 12px !important;
    border-radius: 8px !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--text-primary) !important;
    background: var(--glass-bg) !important;
}

/* ── Glass Card ────────────────────────────────────────────────── */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: var(--glass-shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
}

/* ── Metric Cards ──────────────────────────────────────────────── */
.metric-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}

.metric-card.indigo::before  { background: linear-gradient(90deg, #6C63FF, #818CF8); }
.metric-card.emerald::before { background: linear-gradient(90deg, #10B981, #34D399); }
.metric-card.amber::before   { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
.metric-card.rose::before    { background: linear-gradient(90deg, #EF4444, #F87171); }
.metric-card.purple::before  { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }

.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f9fafb, #d1d5db);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin-bottom: 4px;
}

.metric-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Spec Badge ────────────────────────────────────────────────── */
.spec-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.spec-badge.cs { background: rgba(108,99,255,0.15); color: #818CF8; border: 1px solid rgba(108,99,255,0.3); }
.spec-badge.ds { background: rgba(16,185,129,0.15); color: #34D399; border: 1px solid rgba(16,185,129,0.3); }
.spec-badge.ai { background: rgba(245,158,11,0.15); color: #FBBF24; border: 1px solid rgba(245,158,11,0.3); }
.spec-badge.cy { background: rgba(239,68,68,0.15); color: #F87171; border: 1px solid rgba(239,68,68,0.3); }
.spec-badge.ga { background: rgba(139,92,246,0.15); color: #A78BFA; border: 1px solid rgba(139,92,246,0.3); }

/* ── Hero Header ───────────────────────────────────────────────── */
.hero-header {
    text-align: center;
    padding: 40px 20px 30px;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6C63FF 0%, #EC4899 50%, #F59E0B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
    max-width: 600px;
    margin: 0 auto;
}

/* ── Section Headers ───────────────────────────────────────────── */
.section-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--glass-border);
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Student Profile Card ──────────────────────────────────────── */
.student-card {
    background: linear-gradient(135deg, rgba(108,99,255,0.05), rgba(139,92,246,0.05));
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 20px;
    padding: 28px;
    position: relative;
}

.student-name {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.student-meta {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 16px;
}

.student-gpa {
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent-indigo);
}

/* ── Closing Merit Card ────────────────────────────────────────── */
.closing-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
}

.closing-card:hover {
    transform: scale(1.02);
    border-color: rgba(255,255,255,0.15);
}

.closing-spec {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.closing-name {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.closing-gpa {
    font-size: 1.6rem;
    font-weight: 800;
}

/* ── Status Indicators ─────────────────────────────────────────── */
.status-got-first {
    background: rgba(16,185,129,0.15);
    color: #34D399;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

.status-got-other {
    background: rgba(245,158,11,0.15);
    color: #FBBF24;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

.status-unallocated {
    background: rgba(239,68,68,0.15);
    color: #F87171;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

.status-no-data {
    background: rgba(107,114,128,0.15);
    color: #9CA3AF;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

/* ── Data tables ───────────────────────────────────────────────── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
}

div[data-testid="stDataFrame"] > div {
    border-radius: 12px !important;
}

/* ── Streamlit element overrides ───────────────────────────────── */
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stRadio"] label,
div[data-testid="stTextInput"] label {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: var(--glass-bg);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--glass-border);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--accent-indigo) !important;
    color: white !important;
}

/* ── Divider ───────────────────────────────────────────────────── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
    margin: 24px 0;
}

/* ── Animations ────────────────────────────────────────────────── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeInUp 0.5s ease-out forwards;
}

/* ── Career / Course cards ─────────────────────────────────────── */
.career-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 24px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.career-card:hover {
    border-color: var(--accent-indigo);
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(108,99,255,0.15);
}

.career-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
}

.career-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* ── Skill pill ────────────────────────────────────────────────── */
.skill-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    background: rgba(108,99,255,0.1);
    color: #818CF8;
    border: 1px solid rgba(108,99,255,0.2);
    margin: 3px;
}

/* ── Progress bar custom ───────────────────────────────────────── */
.seat-bar-container {
    background: rgba(255,255,255,0.05);
    border-radius: 8px;
    height: 28px;
    overflow: hidden;
    position: relative;
    margin: 4px 0;
}

.seat-bar-fill {
    height: 100%;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    color: white;
    transition: width 0.8s ease;
}
</style>
"""


def inject_css():
    """Call this at the top of every page to inject the theme."""
    import streamlit as st
    st.markdown(GOOGLE_FONT_IMPORT, unsafe_allow_html=True)
    st.markdown(MAIN_CSS, unsafe_allow_html=True)


def metric_card(value: str, label: str, color_class: str = "indigo") -> str:
    """Return HTML for a single metric card."""
    return f"""
    <div class="metric-card {color_class}">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def spec_badge(spec_name: str) -> str:
    """Return HTML badge for a specialization."""
    from data.models import SPECIALIZATIONS
    code = SPECIALIZATIONS.get(spec_name, {}).get("code", "").lower()
    emoji = SPECIALIZATIONS.get(spec_name, {}).get("emoji", "")
    short = SPECIALIZATIONS.get(spec_name, {}).get("code", spec_name[:2])
    return f'<span class="spec-badge {code}">{emoji} {short}</span>'


def section_header(emoji: str, text: str) -> str:
    """Return HTML for a section header."""
    return f'<div class="section-header">{emoji} {text}</div>'


def status_badge(alloc_choice: int, allocated: str) -> str:
    """Return an HTML status badge based on allocation result."""
    if allocated == "No Data":
        return '<span class="status-no-data">📭 No Data</span>'
    if allocated == "Unallocated":
        return '<span class="status-unallocated">❌ Unallocated</span>'
    if alloc_choice == 1:
        return '<span class="status-got-first">✅ Got 1st Choice</span>'
    return f'<span class="status-got-other">⚠️ Got Choice #{alloc_choice}</span>'
