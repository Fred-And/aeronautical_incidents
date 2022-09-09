from ntpath import join
import pandas as pd
import pydeck as pdk
import streamlit as st

@st.cache
def load_data():

    df = pd.read_csv('aeronautical_incidents.csv')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    #df = df.values()

    return df

# Loading data
df = load_data()

labels = df['type'].unique().tolist()

print(df.dtypes)
## SIDEBAR ##

# Number of found data given a set of filters
st.sidebar.header('Parameters')
info_sidebar = st.sidebar.empty()

# Year selector slidebar
st.sidebar.subheader('Year')
year_to_filter = st.sidebar.slider('Choose the year',2008,2018,2017)

# Checkbox for raw data
st.sidebar.subheader('Spreadsheet')
tabela = st.sidebar.empty()

# SelectBox for filtering classification
label_to_filter = st.sidebar.multiselect(
    label = "Choose the incident type",
    options=labels,
    default=['OUTROS'])

# Checkbox for incident type
st.sidebar.subheader('Filter by incident type')
type_filter = st.sidebar.empty()

# Sidebar Markdown
st.sidebar.markdown(""" The database of aeronautical incidents is managed and provided by the ***Aeronautical Incident Investigation Center (CENIPA)***.""")

# FILTER BEING APPLIED
filtered_df = df.loc[(df['date'].dt.year == year_to_filter) & (df['type'].isin(label_to_filter))]

# Info sidebar filled with data
info_sidebar.info(f'{filtered_df.shape[0]} incident matches')



## MAIN ##

# Main Title
st.title('CENIPA - Aeronautical Incidents')

# Subtitle
st.markdown(f"""
            The displayed incidents are all classified as **{','.join(label_to_filter)}** in: **{year_to_filter}**
            """)

# Dataframe
if tabela.checkbox('Show spreadsheet data'):
    st.write(filtered_df)

# Map
st.subheader('Map of incidents')
st.map(filtered_df,)
