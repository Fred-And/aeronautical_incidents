from ntpath import join
import pandas as pd
import pydeck as pdk
import streamlit as st

@st.cache
def load_data():
    columns = {
        'ocorrencia_latitude':'latitude',
        'ocorrencia_longitude':'longitude',
        'ocorrencia_dia' : 'data',
        'ocorrencia_classificacao':'classificacao',
        'ocorrencia_tipo':'tipo',
        'ocorrencia_tipo_categoria':'tipo_categoria',
        'ocorrencia_tipo_icao':'tipo_icao',
        'ocorrencia_aerodromo':'aerodromo',
        'ocorrencia_cidade':'cidade',
        'investigacao_status':'status',
        'divulgacao_relatorio_numero':'relatorio_numero',
        'total_aeronaves_envolvidas':'aeronaves_envolvidas'
    }

    df = pd.read_csv('ocorrencias_aeronauticas.csv', index_col='codigo_ocorrencia')

    df = df.rename(columns=columns)
    df['data'] = pd.to_datetime(df['data'],format='%Y-%m-%d')
    df = df[list(columns.values())]

    return df

# Loading data
df = load_data()
labels = df['classificacao'].unique().tolist()

## SIDEBAR ##

# Number of found data given a set of filters
st.sidebar.header('Parâmetros')
info_sidebar = st.sidebar.empty()

# Year selector slidebar
st.sidebar.subheader('Ano')
year_to_filter = st.sidebar.slider('Escolha o ano desejado',2008,2018,2017)

# Checkbox for raw data
st.sidebar.subheader('Tabela')
tabela = st.sidebar.empty()

# SelectBox for filtering
label_to_filter = st.sidebar.multiselect(
    label = "Escolha a classificação da ocorrência",
    options=labels,
    default=['INCIDENTE','ACIDENTE']

)

# Sidebar Markdown
st.sidebar.markdown(""" A base de dados de ocorrencias aeronáuticas é gerenciada pelo ***Centro de Investigação de Incidentes Aeronáuticos (CENIPA)***.""")

# FILTER BEING APPLIED
filtered_df = df.loc[(df['data'].dt.year == year_to_filter) & (df['classificacao'].isin(label_to_filter))]

# Info sidebar filled with data
info_sidebar.info(f'{filtered_df.shape[0]} ocorrências selecionadas')



## MAIN ##

# Main Title
st.title('CENIPA - Ocorrências aeronáuticas')

# Subtitle
st.markdown(f"""
            Estão sendo exibidas as ocorrências classificadas como **{','.join(label_to_filter)}** no ano de: **{year_to_filter}**
            """)

# Dataframe
if tabela.checkbox('Mostrar tabela de dados'):
    st.write(filtered_df)

# Map
st.subheader('Mapa de ocorrências')
st.map(filtered_df,)
