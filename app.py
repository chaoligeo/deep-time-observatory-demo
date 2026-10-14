"""
Deep-time Observatory Demo
Interactive explorer for geological time and sample deep-time records.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Ensure local imports work
sys.path.insert(0, str(Path(__file__).parent))
from utils.time_utils import load_timescale, age_to_interval, format_age

st.set_page_config(
    page_title="Deep-time Observatory Demo",
    page_icon="🪨",
    layout="wide",
)

st.title("Deep-time Observatory Demo")
st.caption("深时观测台 · 科学数据系统演示 · Sample exploration of geological ages and records")

# Load data
@st.cache_data
def load_data():
    timescale = load_timescale("data/geological_timescale.csv")
    records = pd.read_csv("data/sample_records.csv")
    records["age_ma"] = pd.to_numeric(records["age_ma"], errors="coerce")
    return timescale, records

timescale, records = load_data()

# Sidebar filters
st.sidebar.header("Filters")

types = ["All"] + sorted(records["type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("Record type", types)

periods = ["All"] + sorted(timescale[timescale["rank"] == "period"]["name"].tolist())
selected_period = st.sidebar.selectbox("Period (approx.)", periods)

age_min, age_max = st.sidebar.slider(
    "Age range (Ma)",
    min_value=0.0,
    max_value=540.0,
    value=(0.0, 540.0),
    step=1.0,
)

# Apply filters
filtered = records.copy()
if selected_type != "All":
    filtered = filtered[filtered["type"] == selected_type]

if selected_period != "All":
    bounds = timescale[timescale["name"] == selected_period]
    if not bounds.empty:
        p_start = bounds.iloc[0]["start_ma"]
        p_end = bounds.iloc[0]["end_ma"]
        filtered = filtered[
            (filtered["age_ma"] <= p_start) & (filtered["age_ma"] >= p_end)
        ]

filtered = filtered[
    (filtered["age_ma"] >= age_min) & (filtered["age_ma"] <= age_max)
]

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Records")
    display_cols = [
        "id", "type", "name", "age_ma", "min_age_ma", "max_age_ma",
        "locality", "lithology", "taxon_or_unit"
    ]
    st.dataframe(
        filtered[display_cols].sort_values("age_ma", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"{len(filtered)} record(s) shown")

with col2:
    st.subheader("Age distribution")
    if not filtered.empty:
        fig = px.histogram(
            filtered,
            x="age_ma",
            nbins=20,
            title="Age distribution of filtered records",
            labels={"age_ma": "Age (Ma)", "count": "Count"},
        )
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        fig.update_xaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No records match the current filters.")

# Timeline
st.subheader("Timeline view")
if not filtered.empty:
    timeline = filtered.sort_values("age_ma", ascending=False).copy()
    timeline["display"] = timeline.apply(
        lambda r: f"{r['name']} ({r['type']})", axis=1
    )
    fig_tl = go.Figure()
    for _, row in timeline.iterrows():
        fig_tl.add_trace(go.Scatter(
            x=[row["age_ma"]],
            y=[row["display"]],
            mode="markers+text",
            marker=dict(size=12),
            text=[format_age(row["age_ma"])],
            textposition="top center",
            name=row["name"],
            hovertext=f"{row['name']}<br>{row['type']}<br>{format_age(row['age_ma'])}<br>{row.get('locality', '')}",
        ))
    fig_tl.update_layout(
        title="Selected records on geological timeline (older → younger)",
        xaxis_title="Age (Ma)",
        yaxis_title="",
        height=max(400, 30 * len(timeline)),
        showlegend=False,
        xaxis=dict(autorange="reversed"),
        margin=dict(l=200, r=20, t=40, b=40),
    )
    st.plotly_chart(fig_tl, use_container_width=True)
else:
    st.info("Adjust filters to see records on the timeline.")

# Geological timescale reference
with st.expander("Geological timescale reference (excerpt)"):
    st.dataframe(
        timescale[["rank", "name", "start_ma", "end_ma", "parent"]].sort_values("start_ma", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

# Age lookup tool
st.subheader("Age lookup")
lookup_age = st.number_input("Enter an age (Ma)", min_value=0.0, max_value=540.0, value=66.0, step=0.1)
if lookup_age is not None:
    interval = age_to_interval(lookup_age, timescale)
    st.write(f"**{format_age(lookup_age)}** falls within: **{interval or 'Outside loaded timescale'}**")

st.divider()
st.caption(
    "This is a demonstration using synthetic sample data. "
    "It illustrates basic organization and exploration patterns for deep-time scientific data "
    "within the Deep-time Observatory (DDE) framework. "
    "For production use, integrate with authoritative sources such as the International Chronostratigraphic Chart, "
    "PBDB, Macrostrat, GEOROC, and national geological databases."
)
