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
    page_title="Cities",
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
col2.markdown("# Visão Cidades")

def make_sidebar(df):
    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Escolha os Países que Deseja Visualizar as Informações",
        df.loc[:, "country_code"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"]
    )

    return list(countries)
countries = make_sidebar(df)  
with st.container():
    
###############GRAFICO DE TOP 10 CIDADES COM MAIOR NUMERO DE RESTAURANTES CADASTRADOS, POR PAIS#############
    
    def grafico_barra2(df, countries):
        
#Filtra o DataFrame original df pelos países selecionados (isin(countries)) e seleciona as colunas 'restaurant_id', 'city' e 'country_code'. Em seguida, agrupa os dados por 'country_code' e 'city' e conta o número de restaurantes em cada cidade. O resultado é armazenado no DataFrame 'dataframe'
        dataframe = df.loc[df['country_code'].isin(countries), ['restaurant_id', 'city', 'country_code']].groupby(['country_code', 'city']).count().reset_index()
    
# Calcula o total de restaurantes por cidade, usando o DataFrame 'dataframe'. Em seguida, seleciona as 10 cidades com maior número de restaurantes e armazena o resultado no DataFrame 'top_10_cidades'.
        top_10_cidades = dataframe.groupby('city')['restaurant_id'].sum().nlargest(10).reset_index()

#Adiciona a coluna "country_code" ao DataFrame top_10_cidades para que possamos usar essa informação como cor no gráfico de barras. A junção é feita com base na coluna 'city' e utilizando o método de junção 'left'.
        top_10_cidades = top_10_cidades.merge(dataframe[['city', 'country_code']], on='city', how='left')

#: Cria uma figura de gráfico de barras usando o DataFrame top_10_cidades. Define 'city' como o eixo x, 'restaurant_id' como o eixo y e 'country_code' como a cor das barras e legenda. O parâmetro barmode='group' é utilizado para agrupar as barras. Também são definidos os rótulos dos eixos e o título do gráfico.
        fig = px.bar(top_10_cidades, x='city', y='restaurant_id', color='country_code', barmode='group',
                     labels={
                         'restaurant_id': 'Restaurantes',
                         'city': 'Cidades',
                         'country_code': 'País'
                     },
                     width=700, height=400, text='restaurant_id')
        fig.update_traces(textposition='outside', texttemplate='%{text:.2s}')
        fig.update_layout(title={
            'text': 'Top 10 Cidades com Maior Número de Restaurantes'
        })
        st.plotly_chart(fig, use_container_width=True)

    # Chamar a função make_sidebar para criar o filtro e obter a lista de países selecionados
   

    # Chamar a função grafico_barra2 passando a lista de países selecionados
    grafico_barra2(df, countries)

#######################OUTRA OPÇÃO DE GRAFICO####################
 


#def generate_bar_chart(df, countries):
    # Filtra o DataFrame de acordo com os países selecionados
#    filtered_df = df[df['country_code'].isin(countries)]

    # Agrupa os restaurantes por país e cidade e conta a quantidade em cada cidade
#    restaurant_counts = filtered_df.groupby(['country_code', 'city']).size().reset_index(name='counts')

    # Filtra as 10 cidades com maior quantidade de restaurantes
#    top_cities = restaurant_counts.groupby('city')['counts'].sum().nlargest(10)

    # Filtra os dados para incluir apenas as 10 cidades com mais restaurantes
#    filtered_df = restaurant_counts[restaurant_counts['city'].isin(top_cities.index)]

    # Configuração das cores para cada país
#    colors = {
#        "India": "#FF0000",
#        "Australia": "#008000",
#        "Brazil": "#0000FF",
#        "Canada": "#FFA500",
#        "Indonesia": "#800080",
#        "New Zeland": "#FFC0CB",
#        "Philippines": "#FFFF00",
#        "Qatar": "#00FFFF",
#        "Singapure": "#FF4500",
#        "South Africa": "#800000",
#        "Sri Lanka": "#FF1493",
#        "Turkey": "#FFD700",
#        "United Arab Emirates": "#FF69B4",
#        "England": "#800000",
#        "United States of America": "#000080"
#    }

    # Cria um dicionário de cores para os países selecionados
#    selected_colors = {country: colors[country] for country in countries}

    # Cria o gráfico de barras utilizando Altair
#    chart = alt.Chart(filtered_df).mark_bar().encode(
#        x=alt.X('city', title='Cidades'),
#        y=alt.Y('counts', title='Quantidade de Restaurantes'),
#        color=alt.Color('country_code:N', legend=alt.Legend(title='País'), scale=alt.Scale(domain=list(selected_colors.keys()), #range=list(selected_colors.values())))
#    ).properties(
#        width=800,
#        height=400
#    )

    # Exibe o gráfico no Streamlit
#    st.altair_chart(chart)

# Apresenta o título e uma breve descrição
#st.write('Top 10 cidades com mais restaurantes registrados')

# Chama a função para criar a barra lateral de filtros e retorna os países selecionados
#countries = make_sidebar(df)

# Chama a função para gerar o gráfico de barras com base nos países selecionados
#generate_bar_chart(df, countries)

with st.container():
        
    col1, col2 = st.columns(2,gap= 'small' )
    with col1:
###############GRAFICO DE TOP 7 CIDADES COM RESTAURANTES COM MEDIA DE AVALIAÇÃO ACIMA DE 4, POR PAIS#############
        def grafico_barra1(df,countries):
            dataframe =df.loc[(df['country_code'].isin(countries))&(df['aggregate_rating'] >= 4), ['restaurant_id','city','country_code','aggregate_rating']].groupby(['city','country_code']).nunique().reset_index()

            top_7_cidades = dataframe.groupby('city')['restaurant_id'].sum().nlargest(7).reset_index()
            top_7_cidades = top_7_cidades.merge(dataframe[['city', 'country_code','aggregate_rating']], on='city', how='left')
            fig = px.bar(top_7_cidades, x='city', y='restaurant_id', color='country_code', barmode='group',
                     labels={
                         'restaurant_id': 'Restaurantes',
                         'city': 'Cidades',
                         'country_code': 'País'
                     },
                     width=800, height=400, text='restaurant_id')
            fig.update_traces(textposition='outside', texttemplate='%{text:.1s}')
            fig.update_layout(title={'text': 'Top 7 Cidades com retaurantes com média acima de 4, por país'}, uniformtext_minsize=14, uniformtext_mode='show')
            st.plotly_chart(fig, use_container_width=True)
        #uniformtext_minsize=14, uniformtext_mode='show') para definir o tamanho do texto e se vai mostrar ou não o rotulo de dados
  
        

        # Chamar a função grafico_barra2 passando a lista de países selecionados
        grafico_barra1(df, countries)
        
    ###############GRAFICO DE TOP 10 CIDADES COM RESTAURANTES COM MEDIA DE AVALIAÇÃO ABAIXO DE 2,5, POR PAIS#############
        with col2:
            def grafico_barra2(df,countries):
                dataframe3 = df.loc[(df['country_code'].isin(countries)) & (df['aggregate_rating'] <= 2.5),['restaurant_id','city','country_code','aggregate_rating']].groupby(['city','country_code']).nunique().reset_index()
                top_10_cidades = dataframe3.groupby('city')['restaurant_id'].sum().nlargest(10).reset_index()
                top_10_cidades = top_10_cidades.merge(dataframe3[['city', 'country_code','aggregate_rating']], on='city', how='left')
                fig = px.bar(top_10_cidades, x='city', y='restaurant_id', color='country_code', barmode='group',
                         labels={
                             'restaurant_id': 'Restaurantes',
                             'city': 'Cidades',
                             'country_code': 'País'
                         },
                         width=800, height=400, text='restaurant_id')         
                fig.update_traces(textposition='outside', texttemplate='%{text:.1s}')
                fig.update_layout(title={'text': 'Top 7 Cidades com retaurantes com média abaixo de 2.5, por país'}, uniformtext_minsize=14, uniformtext_mode='show')
                st.plotly_chart(fig, use_container_width=True)
            #uniformtext_minsize=14, uniformtext_mode='show') para definir o tamanho do texto e se vai mostrar ou não o rotulo de dados

            # Chamar a função grafico_barra2 passando a lista de países selecionados
            grafico_barra2(df, countries)
            
            
   ###############GRAFICO DE TOP 10 CIDADES COM MAIOR QUANTIDADE DE TIPOS DE CULINÁRIA DISTINTOS#############


with st.container():
    def grafico_barra3(df,countries):
        dataframe4 =df.loc[df['country_code'].isin(countries),['city','cuisines','country_code']].groupby(['city','country_code']).nunique().reset_index()
        top_10_cidades = dataframe4.groupby('city')['cuisines'].sum().nlargest(10).reset_index()
        top_10_cidades = top_10_cidades.merge(dataframe4[['city', 'country_code']], on='city', how='left')
        fig = px.bar(top_10_cidades, x='city', y='cuisines', color='country_code', barmode='group',
                         labels={
                             'cuisines': 'Tipos de culinária',
                             'city': 'Cidades',
                             'country_code': 'País'
                         },
                         width=800, height=400, text='cuisines') 
        fig.update_traces(textposition='outside', texttemplate='%{text:.2s}')
        fig.update_layout(title={'text': 'TOP 10 CIDADES COM MAIOR QUANTIDADE DE TIPOS DE CULINÁRIA DISTINTOS'}, uniformtext_minsize=14, uniformtext_mode='show')
        st.plotly_chart(fig, use_container_width=True)                                      
    grafico_barra3 (df,countries)

    
    
    
    


st.sidebar.markdown("""---""") 

processed_data = pd.read_csv(r'C:\Users\Leticia Furletti\Repos\DATA_SCIENCE\Comunidade_Ds\FTC\project1\leths_food\pages\zomato.csv')
st.sidebar.download_button(
    label="Download da base de dados",
    data=processed_data.to_csv(index=False, sep=";"),
    file_name="zomato.csv",
    mime="text/csv",
)

st.sidebar.markdown("###### Leticia Furletti")

