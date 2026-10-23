"""Private local preview; DO NOT deploy publicly with confidential CSV files."""
import streamlit as st
from survey_eda import load_surveys, count_by_year, feedback_completion, grouped_counts

st.set_page_config(page_title='JOJ Workshop Insights — Private Preview', layout='wide')
st.title('Community Workshop Insights')
st.caption('PRIVATE LOCAL PREVIEW • Aggregate survey records, not unique participants or attendance')

@st.cache_data
def read_data():
    return load_surveys()

try:
    df = read_data()
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc))
    st.stop()

by_year = count_by_year(df)
a, b, c = st.columns(3)
a.metric('Year 1 survey records', int(by_year.loc[by_year['Year'].eq('Year 1'), 'Survey records'].sum()))
b.metric('Year 2 survey records', int(by_year.loc[by_year['Year'].eq('Year 2'), 'Survey records'].sum()))
c.metric('Total survey records', len(df))
st.subheader('Survey responses by year')
st.bar_chart(by_year.set_index('Year'))
st.subheader('Feedback question completion')
completion = feedback_completion(df)
st.dataframe(completion, hide_index=True, use_container_width=True)
st.subheader('Participant characteristics — exploratory')
st.caption('Categories with fewer than 5 records are hidden. Counts are survey records, not necessarily unique people.')
choice = st.selectbox('Choose a breakdown', ['Gender', 'Age', 'Please indicate your current maternal stage or support role.', 'Session Topic'])
counts = grouped_counts(df, choice)
if counts.empty:
    st.info('No categories meet the minimum reporting threshold.')
else:
    st.bar_chart(counts.set_index('Category'))
st.info('Do not publish or deploy this preview until research supervisors approve the disclosure controls and summaries.')
