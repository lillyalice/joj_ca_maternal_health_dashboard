"""
time_series/charts/comorbidities.py

The Escalation of Chronic Comorbidities chart: hypertension and diabetes
diagnosis rates for African American mothers on Medi-Cal, from the CA DHCS notebook.

"""

# importing libraries

import streamlit as st
from streamlit_echarts import st_echarts, JsCode
from time_series.common import CHART_KEY


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
