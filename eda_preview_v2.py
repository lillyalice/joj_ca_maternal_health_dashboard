"""JoJ community insights — local-only review preview. Not approved for public deployment."""
from __future__ import annotations

import pandas as pd
import streamlit as st
from survey_eda import load_surveys, feedback_completion

st.set_page_config(page_title="JoJ | Community Insights (Private)", page_icon="📊", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 2rem;}
.hero {padding: 1.5rem 1.7rem; border-radius: 16px; background: linear-gradient(115deg,#24334d,#435875); color: white; margin-bottom: 1.2rem;}
.hero h1 {color:white; margin:0 0 .35rem 0; font-size:2rem;}
.hero p {color:#e6edf5; margin:0;}
.note {font-size:.91rem; color:#637086;}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>Community Workshop Insights</h1><p>Exploring survey engagement and feedback across two workshop years</p></div>', unsafe_allow_html=True)
st.caption("PRIVATE RESEARCH PREVIEW  •  Survey records ≠ unique participants or verified attendance")

@st.cache_data(show_spinner="Loading local survey data…")
def read_data():
    return load_surveys()

try:
    all_df = read_data()
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc))
    st.stop()

period = st.selectbox("Explore survey period", ["Both years", "Year 1", "Year 2"], index=0)
df = all_df if period == "Both years" else all_df.loc[all_df["Year"] == period]
counts = all_df["Year"].value_counts()
y1 = int(counts.get("Year 1", 0))
y2 = int(counts.get("Year 2", 0))

m1, m2, m3 = st.columns(3)
m1.metric("Year 1 records", f"{y1:,}")
m2.metric("Year 2 records", f"{y2:,}")
m3.metric("Records in selection", f"{len(df):,}")
st.caption("Counts represent submitted survey rows. A person may have submitted more than one survey.")

overview, feedback, demographics = st.tabs(["Overview", "Feedback completion", "Participant characteristics"])
with overview:
    st.subheader("Survey submissions across years")
    chart_df = pd.DataFrame({"Year": ["Year 1", "Year 2"], "Survey records": [y1, y2]}).set_index("Year")
    st.bar_chart(chart_df, height=310)
    st.info("Survey submission totals are not attendance counts. Compare years descriptively; the number of workshops and opportunities to respond may differ.")

with feedback:
    st.subheader("How often were feedback questions answered?")
    completion = feedback_completion(df)
    label_map = {"Like": "What participants liked", "Wish": "What participants wished for", "What_If": "Suggestions for the future", "Share": "Additional reflections"}
    completion["Question"] = completion["Question"].map(label_map)
    st.caption("Completion rate = nonblank responses ÷ survey records in the corresponding year. This does not measure positive or negative sentiment.")
    if not completion.empty:
        plot = completion.pivot(index="Question", columns="Year", values="Completion (%)")
        st.bar_chart(plot, height=340)
        with st.expander("View completion summary table"):
            st.dataframe(completion.rename(columns={"Answered":"Nonblank responses", "Total":"Survey records"}), use_container_width=True, hide_index=True)

with demographics:
    st.subheader("Participant characteristics")
    st.caption("Exploratory summaries only. Categories are shown only when all nonzero categories in the selected breakdown contain at least five records; otherwise the entire breakdown is withheld for review.")
    choices = {"Gender": "Gender", "Age": "Age", "Maternal stage or support role": "Please indicate your current maternal stage or support role.", "Workshop session topic": "Session Topic"}
    selected = st.selectbox("Choose a characteristic", list(choices))
    col = choices[selected]
    vals = df[col].fillna("Not provided").astype(str).str.strip().replace("", "Not provided")
    summary = vals.value_counts().rename_axis("Category").reset_index(name="Survey records")
    # Withhold the *entire* breakdown when small cells are present. This avoids
    # reconstructing suppressed counts from displayed totals and other categories.
    if summary.empty or (summary["Survey records"] < 5).any():
        st.warning("This breakdown contains small groups and is withheld pending research-team disclosure review. Try a different characteristic or period.")
    else:
        st.bar_chart(summary.set_index("Category"), height=350)
        st.caption("Categories reflect original survey responses and have not yet been harmonized or approved for public reporting.")

st.divider()
st.warning("Local research preview only. Do not publish this app, share raw CSVs, or deploy it to a public Streamlit server before supervisor approval and a disclosure review.")
