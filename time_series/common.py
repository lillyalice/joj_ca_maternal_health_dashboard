"""
time_series/common.py

Shared settings used by every chart in the Time Series tab.

"""

# every chart uses the same ECharts key and sits at the same spot on the page, so switching
# charts updates one chart in place instead of rebuilding it; rebuilding briefly shrinks the
# page, which made the browser jump back to the top
CHART_KEY = "ts_chart_view"
