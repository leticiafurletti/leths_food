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
df = pd.read_csv(r'C:\Users\Leticia Furletti\Repos\FTC\project1\pages\zomato.csv')

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
    page_title="Countries",
    page_icon="🌍",
    layout="wide"       #ISSO AUMENTA A PAGINA
)

#image_path = 'C://Users//Leticia Furletti//Repos//FTC//project1'
image = Image.open('visão_empresa_imagem_aula47.png' )
col1, col2 = st.sidebar.columns([1, 4], gap="small")
col1.image(image, width=35)
col2.markdown("# Fome Zero")

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

image_path = r'C:\Users\Leticia Furletti\Repos\FTC\project1\pages\terra_image.png'
image = Image.open(image_path)
col1, col2 = st.columns([1, 10], gap="small")
col1.image(image, width=70)
col2.markdown("# Visão Países")

with st.container():
    def grafico_barra1(df):
#preciso criar um dataframe pra armazenar os dados que quer expor no grafico. Esse meu grafico sera de quantidade de restaurantes( coloquei o count() no final) por pais. Para isso agrupo por pais (groupby('country_code'))
        dataframe = df.loc[:,['restaurant_id', 'country_code']].groupby('country_code').count().sort_values('restaurant_id', ascending = False).reset_index() 
#sort_values serve para deixar o grafico em ordem descrescene ou crescente
#defini que os restaurantes devem estar em cada pais
        dataframe=dataframe.loc[dataframe['country_code'].isin(countries)] #essa função de isin eu uso pra atrelar o filtro ao grafico, quando mudar o fiktro muda o grafico
  
        fig =px.bar(dataframe,x='country_code', y='restaurant_id',labels={
        'country_code': 'Países',
        'restaurant_id': 'Quantidade de Restaurantes'}, width=700, height=400,color_discrete_sequence=px.colors.qualitative.Bold, text='restaurant_id') #color_discrete_sequence=px.colors.qualitative.Bold) serve para colocar cor, depois de qualitative. escrevo o noe da escala de cores que quero usar, nesse caso a Bold. text se refere ao valor que quero q seja exibido dentro do meu grafico (complemento da linha abaixo)
        fig.update_traces(textposition='inside',texttemplate='%{text:.2s}')
#text= 'coluna na qual definira os valores do grafico' e fig.update_traces(textposition='inside',texttemplate='%{text:.2s}') .2s significa quantas casas quero depois da virula (nesse caso escolhi duasS
    
        fig.update_layout(title={
        'text' : 'Quantidade de restaurantes por país'})

        st.plotly_chart(fig , use_container_width=True)
    grafico_barra1(df) 

with st.container():
    def grafico_barra2(df):
        dataframe1 = df.loc[:,['city','country_code']].groupby('country_code').nunique().sort_values('city', ascending = False).reset_index()
        dataframe1 = dataframe1.loc[dataframe1['country_code'].isin(countries)]
        
        
        fig1 =px.bar(dataframe1, x='country_code', y= 'city', labels = {
        'country_code': 'Países',
        'city': 'Quantidade de Cidades'}, width=700, height=400,color_discrete_sequence=px.colors.qualitative.Bold, text= 'city') 
        fig1.update_traces(textposition='inside',texttemplate='%{text:.1s}')
        fig1.update_layout(title={
        'text' : 'Quantidade de cidades por país'})
        st.plotly_chart(fig1 , use_container_width=True)
       
    grafico_barra2(df) 


with st.container():
    col1, col2 = st.columns(2 , gap='small' )
    with col1:
        def grafico_barra2(df):
            dataframe1 = df.loc[:,['votes','country_code']].groupby('country_code').mean().sort_values('votes', ascending = False).reset_index()
            dataframe1 = dataframe1.loc[dataframe1['country_code'].isin(countries)]
        
            fig1 =px.bar(dataframe1, x='country_code', y= 'votes', labels = {
            'country_code': 'Países',
            'votes': 'Quantidade de avaliações'}, width=700, height=400,color_discrete_sequence=px.colors.qualitative.Bold, text= 'votes') 
            fig1.update_traces(textposition='inside',texttemplate='%{text:.2s}')
            fig1.update_layout(title={
            'text' : 'Média de avaliações por país'})
            st.plotly_chart(fig1 , use_container_width=True)
       
        grafico_barra2(df) 
        
    with col2:
        def grafico_barra3(df):
            dataframe2 = df.loc[:,['average_cost_for_two','country_code']].groupby('country_code').mean().sort_values('average_cost_for_two', ascending = False).reset_index()
            dataframe2 = dataframe2.loc[dataframe2['country_code'].isin(countries)]
        
            fig2 =px.bar(dataframe2, x='country_code', y= 'average_cost_for_two', labels = {
            'country_code': 'Países',
            'average_cost_for_two': 'Média de preço de um prato para dois'}, width=700, height=400,color_discrete_sequence=px.colors.qualitative.Bold, text= 'average_cost_for_two') 
            fig2.update_traces(textposition='outside',texttemplate='%{text:.2s}')
            fig2.update_layout(title={
            'text' : 'Preço de um prato para dois por país'})
            st.plotly_chart(fig2 , use_container_width=True)
       
        grafico_barra3(df) 
                
