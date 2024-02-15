from haversine import haversine
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
import inflection
import matplotlib.pyplot as plot
import altair as alt
df = pd.read_csv(r'C:\Users\Leticia Furletti\Repos\DATA_SCIENCE\Comunidade_Ds\FTC\project1\leths_food\pages\zomato.csv')

##LIMPANDO DATA FRAME##
#print(df)
#print(df.dtypes)
#print(df.isna().sum())
#print(list(df["Cuisines"].unique()))
#print(df["Cuisines"].value_counts())
df["Cuisines"]=df["Cuisines"].fillna('Pizza, Fast Food')
#print(df.isna().sum())

#tira espaço e coloca underline (underscore(x))
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
df = rename_columns(df)

#Substituir codigos da coluna country_code por palavras
countries = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    return countries[country_id]
df["country_code"]=df["country_code"].apply(country_name)

#Substituir codigos da coluna price_range por palavras
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
df["price_range"]=df["price_range"].apply(create_price_tye)


#Substituir codigos da coluna rating_colors por palavras
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]
df["rating_color"]=df["rating_color"].apply(color_name)

#Coluna cuisines apresentava mais de um valor por celula, separando-os por virgula. Essa função mantera apenas o primeiro dos valores
df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
                                            
#Design da pagina


st.set_page_config( 
    page_title="Cuisines",
    page_icon="🌍",
    layout="wide"       #ISSO AUMENTA A PAGINA
)

#image_path = 'C://Users//Leticia Furletti//Repos//FTC//project1'
image = Image.open('visão_empresa_imagem_aula47.png' )
col1, col2 = st.sidebar.columns([1, 4], gap="small")
col1.image(image, width=35)
col2.markdown("# Fome Zero")



image_path = r'C:\Users\Leticia Furletti\Repos\DATA_SCIENCE\Comunidade_Ds\FTC\project1\leths_food\pages\terra_image.png'
image = Image.open(image_path)
col1, col2 = st.columns([1, 10], gap="small")
col1.image(image, width=70)
col2.markdown("# Visão Culinárias")


def make_sidebar(df):
    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar as Informações",
        df.loc[:, "country_code"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )



#criando filtro de slider na sidebar para selecionar a quantidade de restaurantes
#vou colocar meu comando st.sidebar.slider que serve para me retornr um valor, dentro de uma variavel, que eu escolhi chamar de data_slider
    data_slider = st.sidebar.slider (
        'Selecione a quantidade de Restaurantes que deseja visualizar', 
        value = 1, 
        min_value =1, 
        max_value=20) 


    cuisines = st.sidebar.multiselect(
        "Escolha os Tipos de Culinária ",
        df.loc[:, "cuisines"].unique().tolist(),
        default=[
            "Home-made",
            "BBQ",
            "Japanese",
            "Brazilian",
            "Arabian",
            "American",
            "Italian",
        ],
    )

    return list(countries), data_slider, list(cuisines)
countries, data_slider, cuisines = make_sidebar(df)


processed_data = pd.read_csv(r'C:\Users\Leticia Furletti\Repos\DATA_SCIENCE\Comunidade_Ds\FTC\project1\leths_food\pages\zomato.csv')
st.sidebar.download_button(
    label="Download da base de dados",
    data=processed_data.to_csv(index=False, sep=";"),
    file_name="zomato.csv",
    mime="text/csv",
)

st.sidebar.markdown("###### Leticia Furletti")

df_filtered = df.loc[(df['country_code'].isin(countries)) & (df['cuisines'].isin(cuisines))]
df_filtered = df_filtered.head(data_slider)

with st.container():
    st.title(f" Top {data_slider} Restaurantes")
    df_filtered = df.loc[(df['country_code'].isin(countries)) & (df['cuisines'].isin(cuisines)), ['restaurant_id', 'restaurant_name', 'city', 'average_cost_for_two', 'aggregate_rating', 'votes', 'country_code', 'cuisines']]
    df_filtered = df_filtered.head(data_slider)
    st.dataframe(df_filtered)