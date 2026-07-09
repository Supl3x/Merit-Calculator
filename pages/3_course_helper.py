import streamlit as st
from data.course_data import COURSE_DATA
from data.models import SPECIALIZATIONS
from utils.styles import inject_css, section_header, spec_badge

st.set_page_config(page_title="Course Helper", page_icon="📚", layout="wide")
inject_css()

st.markdown('<div class="hero-header"><h1 class="hero-title">Course Outline Helper</h1><p class="hero-subtitle">Explore core foundations and specialization-specific courses.</p></div>', unsafe_allow_html=True)

# ── Foundation ────────────────────────────────────────────────────────────────
st.markdown(section_header("🧱", "Core Foundation (Years 1-2)"), unsafe_allow_html=True)
st.markdown(f"<p style='color: var(--text-secondary);'>{COURSE_DATA['Core Foundation (Years 1-2)']['description']}</p>", unsafe_allow_html=True)

foundation_courses = COURSE_DATA["Core Foundation (Years 1-2)"]["courses"]
num_cols = 3
cols = st.columns(num_cols)
for i, course in enumerate(foundation_courses):
    with cols[i % num_cols]:
        st.markdown(f"""
        <div class="glass-card" style="padding: 12px 16px; margin-bottom: 12px; font-weight: 500;">
            ✓ {course}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

# ── Specializations ───────────────────────────────────────────────────────────
st.markdown(section_header("🎯", "Specialization Core Courses (Years 3-4)"), unsafe_allow_html=True)
st.markdown("<p style='color: var(--text-secondary); margin-bottom: 24px;'>Select a specialization to view its unique core courses.</p>", unsafe_allow_html=True)

spec_names = list(COURSE_DATA["Specializations"].keys())
tabs = st.tabs([spec.replace('Computer Science - (No Specialisation)', 'CS (No Spec)') for spec in spec_names])

for i, spec in enumerate(spec_names):
    with tabs[i]:
        spec_info = COURSE_DATA["Specializations"][spec]
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid {SPECIALIZATIONS[spec]['color']};">
            <h3 style="margin-top: 0; display: flex; align-items: center; gap: 10px;">
                {SPECIALIZATIONS[spec]['emoji']} {spec}
            </h3>
            <p style="color: var(--text-secondary); margin: 0;">{spec_info['focus']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Core Courses")
        course_cols = st.columns(2)
        
        for j, course in enumerate(spec_info["core_courses"]):
            with course_cols[j % 2]:
                st.markdown(f"""
                <div class="glass-card" style="padding: 12px 16px; margin-bottom: 12px;">
                    <span style="color: {SPECIALIZATIONS[spec]['color']}; margin-right: 8px;">▶</span> {course}
                </div>
                """, unsafe_allow_html=True)

# Note about electives
st.info("💡 Note: Each specialization also requires selecting 5 Elective courses from a pool specific to that track, allowing you to further customize your degree.")
