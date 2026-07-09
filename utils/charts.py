# ── Merit Calculator — Plotly Charts ──────────────────────────────────────────
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data.models import SPECIALIZATIONS, COLOR_SEQUENCE, NO_RESPONSE

# Standard dark theme layout template
LAYOUT_TEMPLATE = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9ca3af", family="Inter"),
    margin=dict(l=20, r=20, t=40, b=20),
)

def create_allocation_bar(remaining_seats: dict) -> go.Figure:
    """Horizontal stacked bar showing filled vs. remaining seats."""
    specs = list(SPECIALIZATIONS.keys())
    filled = [SPECIALIZATIONS[s]["seats"] - remaining_seats.get(s, 0) for s in specs]
    remaining = [remaining_seats.get(s, 0) for s in specs]
    
    fig = go.Figure()
    
    # Filled Seats
    fig.add_trace(go.Bar(
        y=specs,
        x=filled,
        name='Filled Seats',
        orientation='h',
        marker=dict(color=COLOR_SEQUENCE),
        text=filled,
        textposition='inside',
        insidetextanchor='middle'
    ))
    
    # Remaining Seats
    fig.add_trace(go.Bar(
        y=specs,
        x=remaining,
        name='Available Seats',
        orientation='h',
        marker=dict(color='rgba(255, 255, 255, 0.1)', line=dict(color=COLOR_SEQUENCE, width=1)),
        text=remaining,
        textposition='inside',
        insidetextanchor='middle'
    ))
    
    fig.update_layout(
        barmode='stack',
        **LAYOUT_TEMPLATE,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(autorange="reversed") # Highest at top
    )
    return fig

def create_gpa_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram of CGPA distribution."""
    # Filter out 0.0 GPA
    valid_df = df[df["cgpa"] > 0]
    
    fig = px.histogram(
        valid_df, 
        x="cgpa", 
        nbins=30,
        color_discrete_sequence=["#6C63FF"]
    )
    fig.update_layout(
        title="Batch CGPA Distribution",
        xaxis_title="CGPA",
        yaxis_title="Count",
        **LAYOUT_TEMPLATE,
        bargap=0.1
    )
    return fig

def create_specialization_pie(df: pd.DataFrame, choice_col: str = "choice_1") -> go.Figure:
    """Donut chart of choices."""
    counts = df[df[choice_col] != NO_RESPONSE][choice_col].value_counts().reset_index()
    counts.columns = ["Specialization", "Count"]
    
    fig = px.pie(
        counts, 
        values="Count", 
        names="Specialization",
        hole=0.6,
        color="Specialization",
        color_discrete_map={k: v["color"] for k, v in SPECIALIZATIONS.items()}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title=f"{choice_col.replace('_', ' ').title()} Preferences",
        showlegend=False,
        **LAYOUT_TEMPLATE
    )
    return fig

def create_section_breakdown(df: pd.DataFrame) -> go.Figure:
    """Grouped bar for section allocations."""
    # Group by section and allocated spec
    allocated_df = df[~df["allocated"].isin(["No Data", "Unallocated"])]
    counts = allocated_df.groupby(["section", "allocated"]).size().reset_index(name="Count")
    
    fig = px.bar(
        counts, 
        x="section", 
        y="Count", 
        color="allocated",
        barmode="group",
        color_discrete_map={k: v["color"] for k, v in SPECIALIZATIONS.items()}
    )
    fig.update_layout(
        title="Allocations by Section",
        xaxis_title="Section",
        yaxis_title="Number of Students",
        **LAYOUT_TEMPLATE
    )
    return fig

def create_spec_by_section_breakdown(df: pd.DataFrame) -> go.Figure:
    """Grouped bar for specialization allocations broken down by section."""
    allocated_df = df[~df["allocated"].isin(["No Data", "Unallocated"])]
    
    # Sort section so colors are consistent and ordered
    counts = allocated_df.groupby(["allocated", "section"]).size().reset_index(name="Count")
    counts = counts.sort_values(by="section")
    
    # Use a generic color sequence for sections
    section_colors = px.colors.qualitative.Pastel
    
    fig = px.bar(
        counts, 
        x="allocated", 
        y="Count", 
        color="section",
        barmode="group",
        color_discrete_sequence=section_colors
    )
    
    # Clean up x-axis labels
    fig.update_xaxes(tickvals=list(SPECIALIZATIONS.keys()), ticktext=[s.replace('Computer Science - (No Specialisation)', 'CS') for s in SPECIALIZATIONS.keys()])
    
    fig.update_layout(
        title="Section Breakdown per Specialization",
        xaxis_title="Specialization",
        yaxis_title="Number of Students",
        **LAYOUT_TEMPLATE
    )
    return fig
