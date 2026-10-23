"""
time_series/charts/payer.py

The Structural Layering of Maternal Risk chart: Medi-Cal share of births and
hypertension rates by payer, from the CA DHCS notebook.

"""

# importing libraries

import streamlit as st
from streamlit_echarts import st_echarts, JsCode
from time_series.common import CHART_KEY


def render_payer_chart(rates, compare_private):
    """ draws the Structural Layering of Maternal Risk chart

    Bars show Medi-Cal's share of births to African American mothers, with
    hypertension rates as lines on a second axis, from the CA DHCS notebook.
    The notebook has two versions: Medi-Cal only, and Medi-Cal vs. private
    (Non-Medi-Cal) insurance. Statewide only.

    Parameters
    ----------
    rates : DataFrame
        output of load_medi_cal_rates()
    compare_private : bool
        True for the Medi-Cal vs. private version, False for Medi-Cal only

    Returns
    -------
    None.
    """

    medi = rates[rates['payer'] == 'Medi-Cal'].sort_values('year').set_index('year')
    private = rates[rates['payer'] == 'Non-Medi-Cal'].sort_values('year').set_index('year')
    years = medi.index.tolist()

    # titles from the notebook's two versions of this chart
    subtitle = ("Medi-Cal Volume Dominance vs. Payer Hypertension Divergence" if compare_private
                else "Medi-Cal Volume Dominance & Escalating Safety-Net Hypertension Rates")
    st.markdown(f"**The Structural Layering of Maternal Risk in California (2014–2023)**  \n{subtitle}")

    def rounded(col, df):
        return [round(v, 1) for v in df[col]]

    # background bars on the left axis, labeled as in each notebook version
    series = [{
        "name": "Medi-Cal Share of Total Births" if compare_private else "% of Black Births Financed by Medi-Cal",
        "type": "bar", "barWidth": "60%", "data": rounded('medi_cal_share', medi),
        "itemStyle": {"color": "#e0e0e0", "opacity": 0.6},
    }]

    medi_line = {
        "name": "Medi-Cal (Public Safety Net)" if compare_private else "Maternal Hypertension Rate (Medi-Cal)",
        "type": "line", "yAxisIndex": 1, "symbol": "circle", "symbolSize": 8,
        "data": rounded('hypertension_rate', medi),
        "lineStyle": {"width": 3.5, "color": "#d95f02"}, "itemStyle": {"color": "#d95f02"},
    }

    if compare_private:
        # notebook annotation over the years where the two lines split
        medi_line["markArea"] = {
            "silent": True, "itemStyle": {"color": "rgba(0,0,0,0.04)"},
            "label": {"show": True, "position": "insideTop", "fontWeight": "bold", "color": "#333",
                      "backgroundColor": "#fff", "borderColor": "#999", "borderWidth": 1, "padding": 4,
                      "formatter": "The Post-2020\nStructural Divergence"},
            "data": [[{"xAxis": "2020"}, {"xAxis": "2022"}]],
        }
        series.append(medi_line)
        series.append({
            "name": "Non-Medi-Cal (Private/Commercial)", "type": "line", "yAxisIndex": 1,
            "symbol": "rect", "symbolSize": 8, "data": rounded('hypertension_rate', private),
            "lineStyle": {"width": 2.5, "type": "dashed", "color": "#1f77b4"}, "itemStyle": {"color": "#1f77b4"},
        })
    else:
        # notebook annotation on the 2023 peak
        last = years[-1]
        medi_line["markPoint"] = {
            "symbolSize": 0,
            "label": {"show": True, "position": "left", "fontWeight": "bold", "color": "#000",
                      "backgroundColor": "#fff", "borderColor": "#999", "borderWidth": 1, "padding": 4,
                      "formatter": f"Surged to {medi.loc[last, 'hypertension_rate']:.1f}% in {last}\n(Nearly 1 in 4 Mothers)"},
            "data": [{"coord": [str(last), round(medi.loc[last, 'hypertension_rate'], 1)]}],
        }
        series.append(medi_line)

    right_axis_color = "#000" if compare_private else "#d95f02"

    # EChart configuration; axis ranges, labels and colors follow the notebook
    options = {
        "tooltip": {"trigger": "axis", "valueFormatter": JsCode("function (v) { return v.toFixed(1) + '%'; }").js_code},
        "legend": {"data": [s["name"] for s in series], "left": 80, "top": 30, "orient": "vertical"},
        "toolbox": {
            "show": True, "left": "left", "top": "top",
            "feature": {"dataView": {"readOnly": True}, "saveAsImage": {}},
        },
        "grid": {"left": 70, "right": 70, "top": 40, "bottom": 50},
        "xAxis": {"type": "category", "data": [str(y) for y in years],
                  "name": "Calendar Year", "nameLocation": "middle", "nameGap": 30},
        "yAxis": [
            {"type": "value", "min": 0, "max": 100, "name": "Medi-Cal Market Share (% of Total Births)",
             "nameLocation": "middle", "nameGap": 45, "nameTextStyle": {"color": "#7f7f7f"},
             "axisLabel": {"formatter": "{value}%", "color": "#7f7f7f"}, "splitLine": {"show": False}},
            {"type": "value", "min": 0, "max": 30, "name": "Hypertension Prevalence Rate (%)",
             "nameLocation": "middle", "nameGap": 45, "nameTextStyle": {"color": right_axis_color},
             "axisLabel": {"formatter": "{value}%", "color": right_axis_color},
             "splitLine": {"lineStyle": {"type": "dashed", "opacity": 0.3}}},
        ],
        "series": series,
    }

    st_echarts(options=options, height="460px", key=CHART_KEY)

    # key takeaway; numbers come from the data
    share_low, share_high = medi['medi_cal_share'].min(), medi['medi_cal_share'].max()
    first, last = years[0], years[-1]
    if compare_private:
        st.info(
            f"**The two payers split after 2020.** From {first} to 2019, hypertension rose for both: "
            f"Medi-Cal from {medi.loc[first, 'hypertension_rate']:.1f}% to {medi.loc[2019, 'hypertension_rate']:.1f}% "
            f"and private insurance from {private.loc[first, 'hypertension_rate']:.1f}% to "
            f"{private.loc[2019, 'hypertension_rate']:.1f}%. After 2020, the Medi-Cal rate climbed to "
            f"{medi.loc[last, 'hypertension_rate']:.1f}% in {last}, while the private rate dropped to "
            f"{private.loc[2021, 'hypertension_rate']:.1f}% in 2021 and was "
            f"{private.loc[last, 'hypertension_rate']:.1f}% in {last}.",
            icon="💡"
        )
    else:
        st.info(
            f"**Medi-Cal covers most Black births, and hypertension among those mothers keeps rising.** "
            f"Medi-Cal paid for {share_low:.1f}–{share_high:.1f}% of births to African American mothers each year, "
            f"and their hypertension rate rose from {medi.loc[first, 'hypertension_rate']:.1f}% in {first} to "
            f"{medi.loc[last, 'hypertension_rate']:.1f}% in {last}, nearly 1 in 4 mothers.",
            icon="💡"
        )

    with st.expander("About this chart"):
        st.markdown(
            "The grey bars show the share of births to African American mothers that Medi-Cal paid for each year "
            "(left axis). The lines show the share of mothers with a hypertension diagnosis recorded at birth, "
            "out of births where the status was known (right axis).\n\n"
            "Hover over a year to see every value. Click an item in the legend to hide or show it. "
            "This data is statewide only."
        )
        if compare_private:
            st.markdown(
                "**About the 2020–2022 private insurance numbers:** In 2020–2022, DHCS reported no births with an "
                "unknown hypertension status for non-Medi-Cal mothers, compared with about 12% in other years "
                "(for example 872 of 7,086 births in 2019). "
                "Those births appear to have been counted as having no hypertension instead, which would lower the "
                "private insurance rate in those years. Part of the drop after 2020 may come from this change in "
                "how the data was recorded. Medi-Cal is barely affected, since its unknown share was under 2%."
            )
