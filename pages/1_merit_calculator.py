import streamlit as st
import pandas as pd

from data.parser import load_data
from data.allocator import allocate_seats, get_student_availability
from data.models import SPECIALIZATIONS, COLOR_SEQUENCE, CHOICE_COLUMNS
from utils.styles import inject_css, metric_card, spec_badge, section_header, status_badge
from utils.charts import (
    create_allocation_bar,
    create_gpa_distribution,
    create_specialization_pie,
    create_section_breakdown,
    create_spec_by_section_breakdown
)

st.set_page_config(page_title="Merit Calculator", page_icon="📊", layout="wide")
inject_css()

# ── Load Data & Allocate ──────────────────────────────────────────────────────
@st.cache_data(ttl="1h", show_spinner="Processing Merit List...")
def get_processed_data():
    df = load_data()
    return allocate_seats(df)

result = get_processed_data()
df = result["allocated_df"]
closing_merit = result["closing_merit"]
remaining_seats = result["remaining_seats"]
seats_at_turn = result["seats_at_turn"]

valid_students = df[df["has_data"]]
total_students = len(df)
eligible_count = len(valid_students)
allocated_count = (valid_students["allocated"] != "Unallocated").sum()
seats_left = sum(remaining_seats.values())
highest_gpa = df["cgpa"].max()

# ── Header & Metrics ──────────────────────────────────────────────────────────
st.markdown('<div class="hero-header"><h1 class="hero-title">Merit Calculator</h1></div>', unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
with m1: st.markdown(metric_card(str(total_students), "Total Students", "indigo"), unsafe_allow_html=True)
with m2: st.markdown(metric_card(str(eligible_count), "Eligible", "emerald"), unsafe_allow_html=True)
with m3: st.markdown(metric_card(str(allocated_count), "Seats Filled", "purple"), unsafe_allow_html=True)
with m4: st.markdown(metric_card(str(seats_left), "Seats Remaining", "amber"), unsafe_allow_html=True)
with m5: st.markdown(metric_card(f"{highest_gpa:.3f}", "Highest CGPA", "rose"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.plotly_chart(create_allocation_bar(remaining_seats), use_container_width=True, config={'displayModeBar': False})
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_lookup, tab_board, tab_filter, tab_analytics = st.tabs([
    "🔍 Smart Lookup", "🚪 Merit Closing Board", "📊 Filter & Explore", "📈 Analytics"
])

# ── Tab 1: Smart Lookup ───────────────────────────────────────────────────────
with tab_lookup:
    st.markdown(section_header("🔍", "Smart Solo Lookup"), unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("Search for a student by Name or Roll Number to see their allocation status and seat availability.")
        search_query = st.text_input("Enter Name or Roll No (e.g. CT-001 or JAVERIA)", placeholder="Search...")
    
    if search_query:
        query = search_query.strip().upper()
        # Filter df
        matches = df[df["roll_no"].str.upper().str.contains(query) | df["name"].str.upper().str.contains(query)]
        
        if len(matches) == 0:
            st.warning("No student found matching that query.")
        else:
            if len(matches) > 1:
                st.info(f"Found {len(matches)} matches. Showing the first one.")
            
            student = matches.iloc[0]
            
            with col2:
                st.markdown(f"""
                <div class="student-card animate-in">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div class="student-meta">{student['roll_no']} • Section {student['section']}</div>
                            <div class="student-name">{student['name']}</div>
                        </div>
                        <div class="student-gpa">{student['cgpa']:.3f}</div>
                    </div>
                    <div style="margin-top: 16px;">
                        {status_badge(student['alloc_choice'], student['allocated'])}
                        <div style="margin-top: 12px;"><strong>Allocated Seat:</strong> {spec_badge(student['allocated']) if student['allocated'] not in ['Unallocated', 'No Data'] else 'None'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### Seat Availability at the Time of Allocation")
            avail = get_student_availability(student, seats_at_turn.get(student.name, {}))
            
            # Display choices
            c_cols = st.columns(5)
            for i, info in enumerate(avail):
                with c_cols[i]:
                    status = "✅ Allocated to you" if student['allocated'] == info['specialization'] else (
                        "🟢 Available" if info['seats_left'] > 0 else "🔴 Full"
                    )
                    
                    choice_text = f"Choice #{info['choice_rank']}" if info['is_in_choices'] else "Not in choices"
                    
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 16px; margin-bottom: 0;">
                        <div style="font-weight: 700; margin-bottom: 8px;">{info['emoji']} {info['specialization'].replace('Computer Science - (No Specialisation)', 'CS')}</div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 8px;">{choice_text}</div>
                        <div class="seat-bar-container">
                            <div class="seat-bar-fill" style="width: {(info['seats_left']/info['total_seats'])*100}%; background: {'var(--accent-emerald)' if info['seats_left'] > 0 else 'var(--accent-rose)'};">
                                {info['seats_left']} left
                            </div>
                        </div>
                        <div style="font-size: 0.8rem; text-align: center; margin-top: 8px;">{status}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ── Tab 2: Merit Closing Board ────────────────────────────────────────────────
with tab_board:
    st.markdown(section_header("🚪", "Closing Merit per Specialization"), unsafe_allow_html=True)
    st.markdown("This board shows the **last student** who secured a seat in each specialization, indicating the **cutoff GPA**.")
    
    b_cols = st.columns(5)
    
    for i, (spec, info) in enumerate(closing_merit.items()):
        color_class = SPECIALIZATIONS[spec]["code"].lower()
        with b_cols[i]:
            st.markdown(f"""
            <div class="closing-card animate-in" style="animation-delay: {i*0.1}s; border-top: 3px solid {SPECIALIZATIONS[spec]['color']};">
                <div style="font-size: 2rem; margin-bottom: 10px;">{SPECIALIZATIONS[spec]['emoji']}</div>
                <div class="closing-spec">{spec.replace('Computer Science - (No Specialisation)', 'CS')}</div>
                <div style="color: var(--text-secondary); font-size: 0.8rem; margin-bottom: 16px;">Cutoff GPA</div>
                <div class="closing-gpa" style="color: {SPECIALIZATIONS[spec]['color']}">{info['cgpa']:.3f}</div>
                <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--glass-border);">
                    <div class="closing-name">{info['name']}</div>
                    <div style="font-size: 0.75rem; color: var(--text-secondary);">{info['roll_no']} • Sec {info['section']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── Tab 3: Filter & Explore ───────────────────────────────────────────────────
with tab_filter:
    st.markdown(section_header("📊", "Interactive Data Explorer"), unsafe_allow_html=True)
    
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        sections = ['All'] + sorted([s for s in df['section'].unique() if s != '?'])
        sel_section = st.multiselect("Group by Section", sections, default=['All'])
    with f2:
        sel_sort = st.radio("Sort by CGPA", ["Descending", "Ascending"], horizontal=True)
    with f3:
        specs = ['All'] + list(SPECIALIZATIONS.keys())
        sel_choice = st.selectbox("Filter by 1st Choice", specs)
    with f4:
        sel_alloc = st.selectbox("Filter by Allocated Seat", ['All', 'Unallocated', 'No Data'] + list(SPECIALIZATIONS.keys()))
        
    # Apply filters
    filtered_df = df.copy()
    if 'All' not in sel_section and sel_section:
        filtered_df = filtered_df[filtered_df['section'].isin(sel_section)]
    if sel_choice != 'All':
        filtered_df = filtered_df[filtered_df['choice_1'] == sel_choice]
    if sel_alloc != 'All':
        filtered_df = filtered_df[filtered_df['allocated'] == sel_alloc]
        
    filtered_df = filtered_df.sort_values(
        ["cgpa", "roll_num"], 
        ascending=[(sel_sort == "Ascending"), True]
    )
    
    display_df = filtered_df[['roll_no', 'name', 'cgpa', 'section', 'allocated', 'alloc_choice', 'is_tied', 'available_at_turn', 'choice_1', 'choice_2', 'choice_3', 'choice_4', 'choice_5']].copy()
    
    # Format for display
    display_df['cgpa'] = display_df['cgpa'].map('{:.3f}'.format)
    
    # Reset index to reflect current filtered ranking
    display_df.reset_index(drop=True, inplace=True)
    display_df.index = display_df.index + 1
    display_df.index.name = "Rank"
    
    st.markdown(f"**Showing {len(display_df)} students**")
    st.dataframe(display_df, use_container_width=True, height=600)
    
    # Export
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered Data (CSV)", csv, "merit_filtered.csv", "text/csv")


# ── Tab 4: Analytics ──────────────────────────────────────────────────────────
with tab_analytics:
    st.markdown(section_header("📈", "Batch Analytics"), unsafe_allow_html=True)
    
    a1, a2 = st.columns(2)
    with a1:
        st.plotly_chart(create_gpa_distribution(df), use_container_width=True)
    with a2:
        st.plotly_chart(create_specialization_pie(df), use_container_width=True)
        
    a3, a4 = st.columns(2)
    with a3:
        st.plotly_chart(create_section_breakdown(df), use_container_width=True)
    with a4:
        st.plotly_chart(create_spec_by_section_breakdown(df), use_container_width=True)
