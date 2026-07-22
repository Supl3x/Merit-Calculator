import streamlit as st
import pandas as pd

from data.parser import load_data
from data.allocator import allocate_seats
from data.models import SPECIALIZATIONS
from utils.styles import inject_css, section_header
from utils.charts import create_new_sections_breakdown

st.set_page_config(page_title="New Sections", page_icon="🎓", layout="wide")
inject_css()

# ── Load Data & Allocate ──────────────────────────────────────────────────────
@st.cache_data(ttl="1h", show_spinner="Processing Merit List...")
def get_processed_data():
    df = load_data()
    return allocate_seats(df)

result = get_processed_data()
df = result["allocated_df"]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-header"><h1 class="hero-title">New Sections Distribution</h1></div>', unsafe_allow_html=True)

st.markdown("This section displays the newly allocated sections (Section A, Section B, etc.) based on merit ranking within each specialization. Each section consists of 50 students.")

s1, s2 = st.columns([1, 2])
with s1:
    st.markdown("### Filters")
    sel_spec_sec = st.selectbox("Select Specialization", ["All"] + list(SPECIALIZATIONS.keys()), key="sec_spec")
    sel_sec_letter = st.multiselect("Filter by New Section", ["A", "B", "C", "D"], default=["A", "B", "C"], key="sec_letter")
    old_sections = ['All'] + sorted([s for s in df['section'].unique() if s != '?'])
    sel_old_sec = st.selectbox("Filter by Old Section", old_sections, key="old_sec")
    sel_gender = st.selectbox("Filter by Gender", ["All", "M", "F", "-"], key="gender")

with s2:
    st.plotly_chart(create_new_sections_breakdown(df), use_container_width=True)
    
sec_df = df[~df["allocated"].isin(["No Data", "Unallocated"])].copy()

def get_gender(roll_no, section):
    if section != 'E':
        return "-"
    try:
        # Extract the numeric part (e.g. 'CT-219' -> 219)
        num = int("".join(filter(str.isdigit, str(roll_no))))
        if (201 <= num <= 219) or num == 248:
            return "F"
        elif 220 <= num <= 250:
            return "M"
    except ValueError:
        pass
    return "-"

sec_df['Gender'] = sec_df.apply(lambda r: get_gender(r['roll_no'], r['section']), axis=1)

if sel_spec_sec != "All":
    sec_df = sec_df[sec_df["allocated"] == sel_spec_sec]
if sel_sec_letter:
    sec_df = sec_df[sec_df["new_section"].isin(sel_sec_letter)]
if sel_old_sec != "All":
    sec_df = sec_df[sec_df["section"] == sel_old_sec]
if sel_gender != "All":
    sec_df = sec_df[sec_df["Gender"] == sel_gender]
    
sec_df = sec_df.sort_values(by=["allocated", "new_section", "cgpa"], ascending=[True, True, False])

display_sec_df = sec_df[['roll_no', 'name', 'cgpa', 'section', 'allocated', 'new_section', 'Gender']].copy()
display_sec_df['cgpa'] = display_sec_df['cgpa'].map('{:.3f}'.format)
display_sec_df.rename(columns={'section': 'Old Section', 'new_section': 'New Section'}, inplace=True)

display_sec_df.reset_index(drop=True, inplace=True)
display_sec_df.index = display_sec_df.index + 1
display_sec_df.index.name = "S.No"

st.markdown(f"**Showing {len(display_sec_df)} students**")
st.dataframe(display_sec_df, use_container_width=True, height=600)

csv_sec = display_sec_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Sections Data (CSV)", csv_sec, "new_sections.csv", "text/csv")
