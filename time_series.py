"""
time_series.py

This file builds the Time Series tab of the California Maternal Health
Disparities Dashboard. It is imported by app.py, and can also be run on
its own while developing with: streamlit run time_series.py

The charts here are interactive versions of the matplotlib charts from
Mali's CA DHCS and CDC maternal health notebooks, keeping their titles.

"""

# importing libraries

import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts, JsCode
from time_series_data import load_ca_births_by_age, load_medi_cal_rates, AGE_LABELS

# matplotlib's reversed viridis colormap sampled at six points, matching the
# notebook's cmap='viridis_r' for the six age brackets (youngest = yellow)
VIRIDIS_R_6 = ['#fde725', '#7ad151', '#22a884', '#2a788e', '#414487', '#440154']

# age brackets named in the Generational Shift key takeaway, drawn at full color in the chart
HIGHLIGHT_BRACKETS = ('20-24 years', '35-39 years')

# every chart uses the same ECharts key and sits at the same spot on the page, so switching
# charts updates one chart in place instead of rebuilding it; rebuilding briefly shrinks the
# page, which made the browser jump back to the top
CHART_KEY = "ts_chart_view"


# caches loaded births data for ease of access
@st.cache_data
def get_ca_births_by_age():
    return load_ca_births_by_age()


# caches Medi-Cal diagnosis rates for ease of access
@st.cache_data
def get_medi_cal_rates():
    return load_medi_cal_rates()


def render_generational_shift_chart(births, area, area_label):
    """ draws the Generational Shift stacked bar chart for one area

    Stacked bars of each age bracket's share of adult births per year,
    from the CA DHCS notebook. CDPH reports age and race separately, so
    this covers mothers of all races.

    Parameters
    ----------
    births : DataFrame
        output of load_ca_births_by_age()
    area : str
        'Fresno' or 'California'
    area_label : str
        place name used in the title, e.g. 'Fresno County'

    Returns
    -------
    None.
    """

    area_df = births[births['COUNTY_NAME_SHORT'] == area]
    years = sorted(area_df['year'].unique())

    # title from the notebook, corrected to say all races and adjusted for the selected area
    st.markdown(
        f"**The Generational Shift: Age Distribution of Adult Mothers Giving Birth in {area_label}**  \n"
        "(All Races, 2014–2024 Residence Data)"
    )

    # one stacked series per age bracket; suppressed cells become None so they show as gaps
    # the two brackets in the key takeaway are drawn at full color and the rest are faded
    series = []
    for idx, label in enumerate(AGE_LABELS.values()):
        bracket = area_df[area_df['age_label'] == label].set_index('year')['pct'].reindex(years)
        series.append({
            "name": label, "type": "bar", "stack": "age",
            "data": [round(v, 1) if pd.notnull(v) else None for v in bracket],
            "itemStyle": {"color": VIRIDIS_R_6[idx], "borderColor": "#000", "borderWidth": 0.5,
                          "opacity": 0.95 if label in HIGHLIGHT_BRACKETS else 0.35},
            "emphasis": {"focus": "series"},
        })

    # tooltip lists every bracket for the hovered year, or points to the explanation when suppressed
    tooltip_formatter = JsCode(
        "function (params) {"
        + "var out = params[0].axisValue;"
        + "params.slice().reverse().forEach(function (p) {"
        + "var v = (p.value == null) ? 'Not published (see About this chart)' : p.value.toFixed(1) + '%';"
        + "out += '<br/>' + p.marker + p.seriesName + ': ' + v;"
        + "});"
        + "return out;"
        + "}"
    ).js_code

    # EChart configuration; axis and legend labels follow the notebook
    options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}, "formatter": tooltip_formatter},
        "legend": {"data": list(AGE_LABELS.values()), "orient": "vertical", "right": 0, "top": "middle"},
        "graphic": [{"type": "text", "right": 0, "top": 95,
                     "style": {"text": "Maternal Age\nBracket", "font": "bold 12px sans-serif"}}],
        "toolbox": {
            "show": True, "left": "left", "top": "top",
            "feature": {"dataView": {"readOnly": True}, "saveAsImage": {}},
        },
        "grid": {"left": 70, "right": 150, "top": 40, "bottom": 50},
        "xAxis": {"type": "category", "data": [str(y) for y in years],
                  "name": "Data Year", "nameLocation": "middle", "nameGap": 30},
        "yAxis": {"type": "value", "max": 100, "name": "Percentage of Annual Adult Births (%)",
                  "nameLocation": "middle", "nameGap": 45, "axisLabel": {"formatter": "{value}%"},
                  "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.3}}},
        "series": series,
    }

    st_echarts(options=options, height="460px", key=CHART_KEY)

    # key takeaway, adapted from the notebook's Key Analytical Finding; numbers follow the selected area
    pct = area_df.pivot(index='year', columns='age_label', values='pct')
    first, last = years[0], years[-1]
    young, older = HIGHLIGHT_BRACKETS
    st.info(
        f"**Births are shifting older.** In {area_label}, mothers aged 20–24 fell from "
        f"{pct.loc[first, young]:.1f}% of adult births in {first} to {pct.loc[last, young]:.1f}% in {last}, "
        f"while mothers aged 35–39 grew from {pct.loc[first, older]:.1f}% to {pct.loc[last, older]:.1f}%.",
        icon="💡"
    )

    with st.expander("About this chart"):
        st.markdown(
            "Each bar is one year and adds up to 100% of births to mothers aged 20 and older. "
            "Each color is an age group, from youngest (yellow, bottom) to oldest (purple, top). "
            "The 20–24 and 35–39 groups are shown in full color to match the key takeaway above.\n\n"
            "Hover over a bar to see the exact percentage for every age group that year. "
            "Click an age group in the legend to hide or show it."
        )

        # explains hidden cells so a gap isn't mistaken for zero; in Fresno, CDPH hides the 45+ count
        # as a complementary cell so the very small under-15 count can't be worked out from the total
        oldest = area_df[area_df['age_label'] == '45 years and over']
        if oldest['births'].isna().any():
            shown = oldest.dropna(subset=['births'])
            st.markdown(
                f"**Why is the 45+ group missing in some years?** To protect privacy, CDPH doesn't publish "
                "counts for very small groups. In years when another age group is hidden, it also hides the "
                "45+ count, so the hidden number can't be figured out by subtracting from the total. "
                f"This happened in {oldest['births'].isna().sum()} of {len(years)} years. The 45+ group is small "
                f"({shown['births'].min():.0f}–{shown['births'].max():.0f} births in the years it was published, "
                f"about {shown['pct'].min():.1f}–{shown['pct'].max():.1f}%), so the other groups' percentages "
                "are hardly affected (about 0.1 percentage points)."
            )


def render_comorbidities_chart(rates):
    """ draws the Escalation of Chronic Comorbidities line chart

    Hypertension and diabetes diagnosis rates for African American mothers
    on Medi-Cal, from the CA DHCS notebook. Statewide only.

    Parameters
    ----------
    rates : DataFrame
        output of load_medi_cal_rates()

    Returns
    -------
    None.
    """

    medi = rates[rates['payer'] == 'Medi-Cal'].sort_values('year')
    years = medi['year'].tolist()

    # title from the notebook
    st.markdown(
        "**The Escalation of Chronic Comorbidities Among African American Mothers on Medi-Cal**  \n"
        "(2014–2023 Longitudinal Safety-Net Data)"
    )

    # labels the same anchor years as the notebook (2014, 2019, 2023) above or below each point
    anchor_years = [2014, 2019, 2023]

    label_fmt = JsCode("function (p) { return p.value.toFixed(1) + '%'; }").js_code

    def line_data(col, position, color):
        return [
            {"value": round(v, 1),
             "label": {"show": y in anchor_years, "position": position, "formatter": label_fmt,
                       "fontWeight": "bold", "color": color}}
            for y, v in zip(years, medi[col])
        ]

    # EChart configuration; colors, markers, labels and axis range follow the notebook
    options = {
        "tooltip": {"trigger": "axis", "valueFormatter": JsCode("function (v) { return v.toFixed(1) + '%'; }").js_code},
        "legend": {"data": ["Hypertension Diagnosis Rate", "Diabetes Diagnosis Rate"], "left": 80, "top": 30,
                   "orient": "vertical"},
        "toolbox": {
            "show": True, "left": "left", "top": "top",
            "feature": {"dataView": {"readOnly": True}, "saveAsImage": {}},
        },
        "grid": {"left": 70, "right": 30, "top": 40, "bottom": 50},
        "xAxis": {"type": "category", "data": [str(y) for y in years],
                  "name": "Calendar Year", "nameLocation": "middle", "nameGap": 30},
        "yAxis": {"type": "value", "min": 0, "max": 30, "name": "Prevalence Rate of Known Diagnoses (%)",
                  "nameLocation": "middle", "nameGap": 45, "axisLabel": {"formatter": "{value}%"},
                  "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.3}}},
        "series": [
            {"name": "Hypertension Diagnosis Rate", "type": "line", "symbol": "circle", "symbolSize": 8,
             "data": line_data('hypertension_rate', 'top', '#d95f02'),
             "lineStyle": {"width": 3, "color": "#d95f02"}, "itemStyle": {"color": "#d95f02"}},
            {"name": "Diabetes Diagnosis Rate", "type": "line", "symbol": "rect", "symbolSize": 8,
             "data": line_data('diabetes_rate', 'bottom', '#1f77b4'),
             "lineStyle": {"width": 3, "color": "#1f77b4"}, "itemStyle": {"color": "#1f77b4"}},
        ],
    }

    st_echarts(options=options, height="460px", key=CHART_KEY)

    # key takeaway; numbers come from the data
    first, last = medi.iloc[0], medi.iloc[-1]
    st.info(
        f"**Hypertension diagnoses are climbing.** Among African American mothers on Medi-Cal, "
        f"the hypertension diagnosis rate rose from {first['hypertension_rate']:.1f}% in {first['year']} to "
        f"{last['hypertension_rate']:.1f}% in {last['year']}, and the diabetes diagnosis rate rose from "
        f"{first['diabetes_rate']:.1f}% to {last['diabetes_rate']:.1f}%.",
        icon="💡"
    )

    with st.expander("About this chart"):
        st.markdown(
            "Each line shows the share of African American mothers on Medi-Cal who had that diagnosis "
            "recorded at birth, out of births where the diagnosis status was known. Births with an unknown "
            "status are left out.\n\n"
            "Hover over a year to see both rates. Click a line in the legend to hide or show it.\n\n"
            "This data is statewide only, so the Fresno County option is turned off for this chart."
        )


def render_time_series_tab():
    """ renders the contents of the Time Series tab

    This function draws everything inside the Time Series tab. Controls for
    this tab live inside the tab itself rather than the sidebar, because the
    sidebar is shared with the County Map tab.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """

    # creates a subheader for the tab
    st.subheader("Maternal Health Trends Over Time", divider="rainbow")

    # chart picker; each option is one chart from Mali's notebooks. Pills are click-only
    # (no text box) and required=True keeps one chart selected at all times
    chart_options = [
        "The Generational Shift (age of mothers)",
        "Escalation of Chronic Comorbidities (Medi-Cal)",
    ]
    chart = st.pills("Choose a chart:", chart_options, default=chart_options[0], required=True, key="ts_chart")

    if chart.startswith("The Generational Shift"):
        births = get_ca_births_by_age()

        # the dashboard's stakeholder is based in Fresno, so the tab compares Fresno with the state
        area_label = st.radio("Show:", ["Fresno County", "California"], horizontal=True, key="ts_area")
        area = 'Fresno' if area_label == "Fresno County" else 'California'

        render_generational_shift_chart(births, area, area_label)

        st.caption("Data source: CDPH Live Birth Profiles by County (2014-2024), by county of residence. "
                   "CDPH reports births by age and by race separately, so age brackets include mothers of all races.")
        if area == 'California':
            st.caption("Statewide figures are the sum of all 58 counties. CDPH suppresses small counts in some "
                       "rural counties, so these totals are slightly low.")

    else:
        # same control in the same spot as the Generational Shift chart (keeps the page layout steady),
        # locked to California because this data is statewide only
        st.radio("Show:", ["Fresno County", "California"], index=1, horizontal=True, disabled=True,
                 key="ts_area_statewide", help="This chart's data is available statewide only.")

        render_comorbidities_chart(get_medi_cal_rates())

        st.caption("Data source: DHCS Medi-Cal Birth Statistics (2014-2023), California resident hospital births. "
                   "Diagnosis data is available statewide only.")


# lets this file be run on its own for development; app.py imports the function instead
if __name__ == "__main__":
    st.set_page_config(page_title='Time Series Preview', layout="wide")
    render_time_series_tab()
