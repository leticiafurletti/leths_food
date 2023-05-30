#Importando bibliotecas
from haversine import haversine
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
import inflection
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

#Importando csv
df = pd.read_csv(r'C:\Users\Leticia Furletti\Repos\FTC\project1\Datasets\zomato.csv')

##Limpeza do data frame

#Substituindo valores em branco (NaN) pelo valor mais utilizado na coluna
#print(df)
#print(df.dtypes)
#print(df.isna().sum())
#print(list(df["Cuisines"].unique()))
#print(df["Cuisines"].value_counts())
df["Cuisines"]=df["Cuisines"].fillna('Pizza, Fast Food')
#print(df.isna().sum())

#Renomear colunas tirando espaço e coloca underline
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
    page_title="Home Page",
    page_icon="🎲",
    layout="wide"       #ISSO AUMENTA A PAGINA
)


#image_path = 'C://Users//Leticia Furletti//Repos//FTC//project1'
image = Image.open('visão_empresa_imagem_aula47.png' )
col1, col2 = st.sidebar.columns([1, 4], gap="small")
col1.image(image, width=35)
col2.markdown("# Leth Food")

#country_options = st.sidebar.multiselect(
#    ' Escolha os Paises que Deseja visualizar os Restaurantes', 
 #   ['Philippines', 'Brazil', 'Australia', 'United States of America',
   #    'Canada', 'Singapure', 'United Arab Emirates', 'India',
    #   'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
     #  'Sri Lanka', 'Turkey'], 
    #default=['Brazil', 'Australia','England', 'Qatar', 'South Africa','Canada'] ) 

def make_sidebar(df):
    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar as Informações",
        df.loc[:, "country_code"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    return list(countries)

countries = make_sidebar(df)
    
st.sidebar.markdown("""---""") 

processed_data = pd.read_csv(r'C:\Users\Leticia Furletti\Repos\FTC\project1\zomato.csv')
st.sidebar.download_button(
    label="Download da base de dados",
    data=processed_data.to_csv(index=False, sep=";"),
    file_name="zomato.csv",
    mime="text/csv",
)

st.sidebar.markdown("###### Leticia Furletti")

st.write( "# Leth Food!" )
st.write( "## O Melhor lugar para encontrar seu mais novo restaurante favorito!" )
st.write( "### Temos as seguintes marcas dentro da nossa plataforma:")


with st.container():
        
    col1, col2, col3, col4,col5 = st.columns([5,5,5,8,7] )
    with col1:
        restaurants_unique = len( df.loc[:, 'restaurant_id'].unique() )
        restaurantes = (f'{restaurants_unique:,f}').replace(",",".")[:5] #função para colocar separador de milhar [:x] é pra colocar a quantidade de numeros (contando com o ponto) 
        col1.metric( 'Restaurantes Cadastrados', restaurantes)
    with col2:
        countries_unique = len(df.loc[:,'country_code'].unique())
        col2.metric('Países Cadastrados', countries_unique)
    with col3:
        cities_unique = len(df.loc[:,'city'].unique())
        col3.metric('Cidades Cadastradas', cities_unique)
    with col4:
        ratings = sum(df.loc[:,'votes'])
        votes = (f'{ratings:,f}').replace(",",".")[:9] #função para colocar separador de milhar [:x] é pra colocar a quantidade de numeros (contando com o ponto) 
        col4.metric('Avaliações Feitas na Plataforma', votes)    
         
    with col5:
        cuisines_unique = len(df.loc[:,'cuisines'].unique())
        col5.metric('Tipos de Culinárias Oferecidas', cuisines_unique)
        
                            
    
    
#st.markdown( "## Country Maps" )

#df_aux = df.loc[:, ['restaurant_id', 'longitude', 'latitude']].groupby( ['restaurant_id'] ).median().reset_index()

#map = folium.Map(zoom_start=11)


#for index, location_info in df_aux.iterrows():
#        folium.Marker( [location_info['latitude'], 
#                 location_info['longitude']],
#                 popup=location_info[['restaurant_id']] ).add_to( map )
    
#folium_static( map, width=1024 , height=600 )


def create_map(df):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in df.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["rating_color"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)
map_df = df.loc[df['country_code'].isin(countries)]

create_map(map_df)   





