import streamlit as st

st.set_page_config(
    page_title="Merit Calculator & Advisor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_css, section_header
inject_css()

# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎓 Merit System")
    st.caption("v1.0 • NED University BSCS")
    st.markdown("---")
    st.page_link("app.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_merit_calculator.py", label="📊 Merit Calculator", icon="📊")
    st.page_link("pages/2_career_advisor.py", label="🎯 Career Advisor", icon="🎯")
    st.page_link("pages/3_course_helper.py", label="📚 Course Helper", icon="📚")

# ── Landing Page ──────────────────────────────────────────────────────────────
st.markdown('<div class="hero-header animate-in">', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Merit Calculator & Advisor</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Interactive seat allocation, career path guidance, and comprehensive course outlines for BS Computer Science students.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="glass-card animate-in" style="animation-delay: 0.1s; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
            <h3 style="margin-bottom: 10px;">Merit Calculator</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">
                See exactly which specialization seats are available, simulate allocations based on CGPA, and view closing merits.
            </p>
        </div>
        """, unsafe_allow_html=True
    )
with col2:
    st.markdown(
        """
        <div class="glass-card animate-in" style="animation-delay: 0.2s; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎯</div>
            <h3 style="margin-bottom: 10px;">Career Advisor</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">
                Map your desired job role to the right specialization, discover required skills, and get elective recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """
        <div class="glass-card animate-in" style="animation-delay: 0.3s; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📚</div>
            <h3 style="margin-bottom: 10px;">Course Helper</h3>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">
                Explore core courses vs specializations, browse electives, and understand CS branching areas based on the prospectus.
            </p>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---")
st.markdown("<p style='text-align: center; color: var(--text-secondary);'>Select a tool from the sidebar to get started.</p>", unsafe_allow_html=True)
