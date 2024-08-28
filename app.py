import streamlit as st
import time
import matplotlib.pyplot as plt
import pandas as pd

url = 'https://catalog.ourworldindata.org/explorers/who/latest/monkeypox/monkeypox.csv'

st.set_page_config(
    page_title="Monkeypox Dashboard",
    page_icon="🐒",
    layout="wide",
)

@st.cache_data
def get_data():
    data = pd.read_csv(url, low_memory=False)
    data = data[['location', 'new_cases', 'date']].dropna()
    data['date'] = pd.to_datetime(data['date'])
    data['year_month'] = data['date'].dt.strftime("%Y-%m")
    geo_dynamics = data.pivot_table(index='location', 
                               columns='year_month', 
                               values='new_cases', 
                               aggfunc='sum').fillna(0)
    return geo_dynamics

data = get_data()

st.title("Monkeypox Dashboard")
default_ix = data.index.tolist().index('Democratic Republic of Congo')
geo_filter = st.selectbox("Select the Geography", data.index, index=default_ix)

placeholder = st.empty()
data = data.loc[geo_filter]

with placeholder.container():
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="Total cases", value=round(data.sum()))
    kpi2.metric(label="Cases per month", value=int(data.mean()))
    
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Case dynamics")
        fig, ax = plt.subplots()
        ax.plot(data.index, data.values)
        plt.xlabel('Year-Month')
        plt.ylabel('Total monkeypox confirmed cases')
        plt.xticks(rotation=90)
        st.pyplot(fig)
        
    st.markdown("### Detailed Data View")
    st.dataframe(data)
    time.sleep(1)