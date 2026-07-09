import streamlit as st
from data.career_data import CAREER_PATHS
from data.models import SPECIALIZATIONS
from utils.styles import inject_css, section_header, spec_badge

st.set_page_config(page_title="Career Advisor", page_icon="🎯", layout="wide")
inject_css()

st.markdown('<div class="hero-header"><h1 class="hero-title">Career Path Advisor</h1><p class="hero-subtitle">Map your dream job to the right degree specialization.</p></div>', unsafe_allow_html=True)

# ── Role Selector ─────────────────────────────────────────────────────────────
st.markdown("### 1. Select a Target Career")
role_names = list(CAREER_PATHS.keys())

# Create a grid of selectable cards
cols = st.columns(len(role_names))
selected_role = st.session_state.get("selected_role", role_names[0])

for i, role in enumerate(role_names):
    info = CAREER_PATHS[role]
    is_selected = role == selected_role
    
    border_color = "var(--accent-indigo)" if is_selected else "var(--glass-border)"
    bg_color = "rgba(108,99,255,0.05)" if is_selected else "var(--glass-bg)"
    
    with cols[i]:
        if st.button(f"{info['icon']} {role.split('/')[0].strip()}", key=f"btn_{i}", use_container_width=True):
            st.session_state.selected_role = role
            st.rerun()

# ── Display Role Info ─────────────────────────────────────────────────────────
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
role_data = CAREER_PATHS[selected_role]

st.markdown(f"<h2>{role_data['icon']} {selected_role}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 24px;'>{role_data['description']}</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown(section_header("🎓", "Recommended Route"), unsafe_allow_html=True)
    
    # Show badges for recommended specs
    badges = " ".join([spec_badge(spec) for spec in role_data['recommended_specs']])
    st.markdown(f"<div style='margin-bottom: 16px;'>{badges}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="glass-card">
        <h4 style="margin-top: 0;">Why this route?</h4>
        <p style="color: var(--text-secondary); line-height: 1.6;">{role_data['why_this_route']}</p>
        <h4 style="margin-top: 24px;">Recommended Electives</h4>
        <ul>
            {''.join([f"<li><span style='color: var(--text-secondary);'>{e}</span></li>" for e in role_data['relevant_electives']])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(section_header("🛠️", "Skill & Career Roadmap"), unsafe_allow_html=True)
    
    # Skills
    skills_html = "".join([f'<span class="skill-pill">{s}</span>' for s in role_data['key_skills']])
    st.markdown(f"""
    <div class="glass-card" style="margin-bottom: 16px;">
        <h4 style="margin-top: 0; margin-bottom: 12px;">Key Skills to Acquire</h4>
        {skills_html}
    </div>
    """, unsafe_allow_html=True)
    
    # Trajectory
    trajectory_steps = role_data['career_trajectory'].split('->')
    steps_html = ""
    for idx, step in enumerate(trajectory_steps):
        steps_html += f"""
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="background: var(--accent-indigo); width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: bold; margin-right: 12px;">{idx+1}</div>
            <div style="font-weight: 500;">{step.strip()}</div>
        </div>
        """
        if idx < len(trajectory_steps) - 1:
            steps_html += '<div style="height: 16px; width: 2px; background: var(--glass-border); margin-left: 11px; margin-bottom: 8px;"></div>'
            
    st.markdown(f"""
    <div class="glass-card">
        <h4 style="margin-top: 0; margin-bottom: 16px;">Career Trajectory</h4>
        {steps_html}
        <div style="margin-top: 20px; padding-top: 16px; border-top: 1px solid var(--glass-border);">
            <div style="font-size: 0.8rem; color: var(--text-secondary);">Avg. Salary Range</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: var(--accent-emerald);">{role_data['salary_range']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
