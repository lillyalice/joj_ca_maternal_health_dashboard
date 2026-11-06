
"""
Community Insights tab for the Jewel of Justice dashboard.

Local research preview only. Not approved for public deployment.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from survey_eda import load_surveys, feedback_completion


@st.cache_data(show_spinner="Loading local survey data...")
def read_community_data():
    return load_surveys()


def render_community_insights_tab():

    # Heading and introduction
    st.subheader(
        "Community Workshop Insights",
        divider="rainbow"
    )

    st.write(
        "Explore survey engagement, participant characteristics, "
        "and feedback from the Year 1 and Year 2 Jewel of Justice workshops."
    )

    st.caption(
        "PRIVATE RESEARCH PREVIEW | "
        "Survey records are not necessarily unique participants "
        "or verified workshop attendance."
    )

    # Load confidential survey data locally
    try:
        all_df = read_community_data()
    except (FileNotFoundError, ValueError):
        st.info(
            "Community Insights data is unavailable in this environment."
        )
        return

    # Year selector
    period = st.selectbox(
        "Explore survey period",
        ["Both years", "Year 1", "Year 2"],
        index=0,
        key="community_period"
    )

    # Filter using the actual column name from survey_eda.py
    if period == "Both years":
        df = all_df
    else:
        df = all_df.loc[all_df["Year"] == period]

    # Count survey records by year
    counts = all_df["Year"].value_counts()

    y1 = int(counts.get("Year 1", 0))
    y2 = int(counts.get("Year 2", 0))

    # Summary metrics
    m1, m2, m3 = st.columns(3)

    m1.metric("Year 1 records", f"{y1:,}")
    m2.metric("Year 2 records", f"{y2:,}")
    m3.metric("Records in selection", f"{len(df):,}")

    st.caption(
        "Counts represent submitted survey rows. "
        "A person may have submitted more than one survey."
    )

    # Inner tabs for EDA sections
    overview, feedback, demographics = st.tabs([
        "Overview",
        "Feedback completion",
        "Participant characteristics"
    ])

    # OVERVIEW
    with overview:
        st.subheader("Survey submissions across years")

        chart_df = pd.DataFrame({
            "Year": ["Year 1", "Year 2"],
            "Survey records": [y1, y2]
        }).set_index("Year")

        st.bar_chart(chart_df, height=310)

        st.info(
            "Survey submission totals are not attendance counts. "
            "The number of workshops and opportunities to respond "
            "may differ between years."
        )

    # FEEDBACK COMPLETION
    with feedback:
        st.subheader("How often were feedback questions answered?")

        completion = feedback_completion(df)

        label_map = {
            "Like": "What participants liked",
            "Wish": "What participants wished for",
            "What_If": "Suggestions for the future",
            "Share": "Additional reflections"
        }

        completion["Question"] = completion["Question"].map(
            label_map
        )

        st.caption(
            "Completion rate = nonblank responses divided by "
            "survey records. This does not measure sentiment."
        )

        if not completion.empty:
            plot = completion.pivot(
                index="Question",
                columns="Year",
                values="Completion (%)"
            )

            st.bar_chart(plot, height=340)

            with st.expander("View completion summary table"):
                st.dataframe(
                    completion.rename(columns={
                        "Answered": "Nonblank responses",
                        "Total": "Survey records"
                    }),
                    use_container_width=True,
                    hide_index=True
                )

    # PARTICIPANT CHARACTERISTICS
    with demographics:
        st.subheader("Participant characteristics")

        st.caption(
            "Exploratory summaries only. A breakdown is withheld "
            "if any nonzero category contains fewer than five records."
        )

        choices = {
            "Gender": "Gender",
            "Age": "Age",
            "Maternal stage or support role":
                "Please indicate your current maternal stage or support role.",
            "Workshop session topic": "Session Topic"
        }

        selected = st.selectbox(
            "Choose a characteristic",
            list(choices),
            key="community_characteristic"
        )

        col = choices[selected]

        vals = (
            df[col]
            .fillna("Not provided")
            .astype(str)
            .str.strip()
            .replace("", "Not provided")
        )

        summary = (
            vals.value_counts()
            .rename_axis("Category")
            .reset_index(name="Survey records")
        )

        # Withhold entire breakdown when small groups are present
        if summary.empty:
                st.info(
                    "No survey records are available for this selection."
                )

        elif (summary["Survey records"] < 5).any():
            st.warning(
                f"The {selected.lower()} breakdown is temporarily "
                "unavailable because one or more categories contain "
                "small groups. This information requires research-team "
                "privacy review before it can be displayed."
            )

        else:
            st.bar_chart(
                summary.set_index("Category"),
                height=350
            )

            st.caption(
                "Categories reflect original survey responses "
                "and have not yet been approved for public reporting."
            )

    st.divider()

    st.warning(
        "Local research preview only. Do not deploy publicly "
        "or share confidential survey files before supervisor "
        "approval and disclosure review."
    )
