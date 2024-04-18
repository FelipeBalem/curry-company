import pandas as pd
from numpy import sin, cos, arccos, pi, round
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import folium_static


#-------------------------------------------------------------------
#Funtion to use in distance functions
#Única função copiada e colada
def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians

def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2, unit = 'miles'):
    
    theta = longitude1 - longitude2
    
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    
    if unit == 'miles':
        return round(distance, 2)
    if unit == 'kilometers':
        return round(distance * 1.609344, 2)
#--------------------------------------------------------------------


def read_df() -> pd.DataFrame:
    """
    Função criada para garantir que o mesmo arquivo será lido em todas as páginas
    """
    df = pd.read_csv("datasets/train_limpo.csv")
    
    return df


def create_column_week_of_year(df1):
    """
        Através da coluna 'Order_Date', cria uma coluna à direita do DF com
        as respectivas semanas de cada data.

        INPUT: dataframe
        OUTPUT: dataframe

        Utiliza a função getDistanceBetweenPoinstNew para descobrir a distância entre latitudes e longitudes
    """
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%Y-%m-%d')
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df1['Week_of_year'] = df1['Week_of_year'].astype(int)

    return df1


def find_max_value(df1, column: str) -> float:
    return df1.loc[:,'Delivery_person_Age'].max()


def find_min_value(df1, column: str) -> float:
    return df1.loc[:,'Delivery_person_Age'].min()

def find_mean_value(df1, column: str) -> float:
    return df1.loc[:,'Delivery_person_Age'].mean()
    

def replace_vehicle_conditions(df1: pd.DataFrame) :
    """
    Troca os valores 0, 1, 2 da coluna Vehicle condition para ruim, regular e excelente, respectivamente
    INPUT: dataframe
    OUTPUT: dataframe
    """
    df1['Vehicle_condition'] = (df1['Vehicle_condition'].replace({0 : 'Bad', 1 : 'Regular', 2: 'Excelent'}))
    return df1


def avg_rating_by(df1, by : str) -> float:
    """
    Retorna a média da avaliação das entregas por 'by'
    INPUT: df1: Dataframe, by: nome da coluna
    OUTPUT: float
    """
    st.markdown('##### Average Rating by {}'.format(by))
    avg_rating = (df1.loc[:,['Delivery_person_Ratings', by]]
                      .groupby(by)
                      .mean()
                      .reset_index())
                
    return avg_rating 

def plot_avg_rating_by(df1, by : str) -> float:
    """
    Variação do avg_rating_by, que escreve um título em markdown nvl5 e retorna um df com a média e desvio padrão das avaliações das entregas por 'by'
    INPUT: df1: Dataframe, by: nome da coluna
    OUTPUT: dataframe
    """
    st.markdown('##### Ratings by {}'.format(by))
    df_avg_ratings_per = (df1.loc[:,['Delivery_person_Ratings',by]]
                               .groupby(by)
                               .agg({'Delivery_person_Ratings': ['mean','std']}))
    
    df_avg_ratings_per.columns = ['Average', 'Standart Variation'] 
    df_avg_ratings_per.reset_index()
    
    return df_avg_ratings_per


def top_10_delivery_men_by(df1, by : str) :
    """
    Retorna uma lista com os top 10 mais rápidos por 'by'
    INPUT: df1: dataframe, by: nome da coluna
    OUTPUT: dataframe com head(10)
    """
    st.markdown('##### Top 10 Fastest Deliveries by {}'.format(by))
    top_10 = (df1.loc[:, [by, 'Delivery_person_ID', 'Time_taken(min)']]
                                               .sort_values(by=[by,'Time_taken(min)'])
                                               .groupby(by)
                                               .head(10)
                                               .reset_index(drop=True))
    return top_10


def last_10_delivery_men_by(df1, by : str):
    """
    Retorna uma lista com os top 10 mais lentos por 'by'
    INPUT: df1: dataframe, by: nome da coluna
    OUTPUT: dataframe com head(10)
    """
    st.markdown('##### Top 10 Slowest Deliveries by {}'.format(by))
    last_10 = (df1.loc[:, [by, 'Delivery_person_ID', 'Time_taken(min)']]
                                                .sort_values(by=[by,'Time_taken(min)'], ascending=False)
                                                .groupby(by)
                                                .head(10)
                                                .reset_index(drop=True))
    return last_10


def avg_deliveries_by(df1, by: str):
    """
    Retorna a média entre entregas e o parâmetro by
    INPUT: dataframe
    OUTPUT: float
    """
    return (df1.loc[:,'ID'].count() / df1.loc[:,by].nunique())


def restaurants_map(df1, groupby: list[str]) :
    """
    Escreve um título markdown nvl 3 e Plota um gráfico com um mapa com pins do lugar médio de maior fluxo de entregas, agrupados por groupby
    """
    st.markdown('### Deliveries location center by {} and {}'.format(groupby[0], groupby[1]))
    cols = groupby + ['Delivery_location_latitude', 'Delivery_location_longitude']
    data_plot = df1.loc[:,cols].groupby(groupby).median().reset_index()
    center_latitude =  df1['Delivery_location_latitude'].mean()
    center_longitude = df1['Delivery_location_longitude'].mean()
    map_ = folium.Map(location = (center_latitude, center_longitude), zoom_start=5, min_zoom=5)
    for index, location_info in data_plot.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], icon=folium.Icon(), popup=location_info[groupby]).add_to(map_)

    folium_static(map_, width=1024, height=600)
            

def number_of_deliveries_per(df1, by: str) -> None:
    """
    Escreve um título em markdown nvl3, retorna um gráfico de lina onde x é a coluna parâmetro passado pelo by e o y é a quantidade de entregas.
    INPUT: df1 -> dataframe, by: nome da coluna
    OUTPUT: None
    OBS: Não é necessário passar ID como parâmetro
    """
    
    st.markdown('### Number of deliveries per {}'.format(by))
    
    df_aux02 = df1.loc[:,['ID', by]].groupby(by).count().reset_index()
    fig = px.line(df_aux02, x=by, y='ID')
    st.plotly_chart(fig, use_container_width=True)



def avg_delivery_per_week_by(df1, by : str) -> None:
    """
    Escreve um título em markdown nvl3, retorna um gráfico de linha com o eixo x sendo a coluna Week_of_year e o eixo y sendo a média de entregas com o parâmetro 'by'
    INPUT -> df1: Dataframe, by: nome da coluna
    OUTPUT -> None
    Obs: NÃO É NECESSÁRIO passar ID nem Week_of_Year
    """

    st.markdown('### Average number of deliveries per {} by Week'.format(by))
        
    df_aux01 = df1.loc[:,[by, 'Week_of_year']].groupby(['Week_of_year']).nunique().reset_index()
    df_aux02 = df1.loc[:,['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index()
    
    df_by_week_delivery_count_by = pd.merge(df_aux02, df_aux01, how='inner')
    df_by_week_delivery_count_by['average_delivery_by'] = df_by_week_delivery_count_by['ID'] / df_by_week_delivery_count_by[by]
    fig = px.line(df_by_week_delivery_count_by, x='Week_of_year', y='average_delivery_by')
        
    st.plotly_chart(fig, use_container_width=True)



def deliveries_by_bar(df1, by: str) -> None:
    """
    Escreve um título do gráfico a ser plotado e 
    Plota um gráfico de barra usando o parâmetro by como eixo X e ID como eixo Y
    Pode ser usado para qualquer coluna da tabela da Curry Company
    INPUT: df1 -> DataFrame, by -> Nome da coluna do data frame
    NÃO É NECESSÁRIO PASSAR ID
    OUTPUT - > NONE
    """
    st.markdown("### Deliveries by {}".format(by))
    cols = [by] + ['ID']
    df_qnt_pedidos_x_dia = df1.loc[:, cols].groupby(by).count().reset_index()
    #df_qnt_pedidos_x_dia.columns = ['Order Date', 'Deliveries']
    fig = px.bar(df_qnt_pedidos_x_dia, x=by, y='ID')
    st.plotly_chart( fig, use_container_width = True) 


def deliveries_by_bar_group(df1, by: list[str]) -> None:
    """
    Escreve um título do gráfico a ser plotado e 
    Plota um gráfico de barra usando o parâmetro by[0] como eixo X, by[1] como color e ID como eixo Y
    Pode ser usado para qualquer coluna da tabela da Curry Company
    INPUT: df1 -> DataFrame, by -> Lista com as coluna do data frame
    NÃO É NECESSÁRIO PASSAR ID
    OUTPUT - > NONE    
    """
    st.markdown('### Deliveries by {} and {}'.format(by[0], by[1]))
    cols = by + ['ID']
    df_aux = df1.loc[:,cols].groupby(by).count().reset_index()

    fig = px.bar(df_aux, x=by[0], y='ID', color=by[1], barmode='group')
    st.plotly_chart(fig, use_container_width=True)


def deliveries_by_pie(df1, by: str) -> None:
    """ 
    Escreve um título do gráfico a ser plotado e
    Plota um gráfico de pizza usando o parâmetro by como cores e ID como valores
    Pode ser usado para qualquer coluna da tabela da Curry Company
    INPUT: df1 -> DataFrame, by -> Nome da coluna do data frame
    NÃO É NECESSÁRIO PASSAR ID
    OUTPUT - > NONE
    """
    st.markdown('### Deliveries % by {}'.format(by))
    cols = [by] + ['ID']
    df_aux= df1.loc[:, cols].groupby(by).count().reset_index()
    df_aux['perc_id'] = df_aux['ID']/df_aux['ID'].sum() * 100
    
    fig = px.pie(df_aux, values='perc_id', names=by)
    st.plotly_chart(fig, use_container_width=True)



def avg_distance_restaurant_client(df1) -> float:
    """
    Usando a função getDistanceBetweenPointsNew, retorna a médio de todas as distâncias no dataframe (arrendondado para 2 casas decimais)
    INPUT: Dataframe
    OUTPUT: Float
    """
    #Average distance between restaurant and client
    df_aux = df1.loc[:,['Restaurant_latitude',
                        'Restaurant_longitude',
                        'Delivery_location_latitude',
                        'Delivery_location_longitude']]
    
    df_aux['Delivery_distance'] = (getDistanceBetweenPointsNew( df_aux['Restaurant_latitude'], 
                                                              df_aux['Restaurant_longitude'],
                                                              df_aux['Delivery_location_latitude'], 
                                                              df_aux['Delivery_location_longitude'], 
                                                              unit = 'kilometers' ))
    avg_distance_restaurant_client = round(df_aux['Delivery_distance'].mean(),2)

    return avg_distance_restaurant_client



def avg_time_delivery_festival(df1, festival:bool) -> float:
    """
    Calcula o tempo médio de entrega durante ou sem festivais, devendo ser passado o parâmetro 'festival'
    INPUT: Dataframe, Boolean
    OUTPUT: Float, arredondado para 2 casas decimais
    """
    #Tempo médio de entraga durante festival
    df_aux = df1.loc[df1['Festival'] == festival]
    avg_time_festival = round(df_aux.loc[:,'Time_taken(min)'].mean(),2)

    return avg_time_festival


def avg_std_time_delivery_group_by(df1, groupby: list[str], color: str=None) :
    
    """
    Plota um gráfico com média e desvio padrão de tempo de entrega com base na lista de agrupamento de colunas informado.
    Pode agrupar por até 2 colunas, para isso, passe o valor de color como a coluna que contém as opções a serem agrupadas.
    O groupby deve ser passado SEMPRE como uma lista com o primeiro valor sendo o que vai no eixo e o segundo o que vai estar em color
    NÃO É NECESSÁRIO PASSAR A COLUNA TIME TAKEN(MIN)
    INPUT: df1 -> DATAFRAME, groupby -> lista de colunas, color -> string da coluna que estará na legenda.
    OUTPUT: fig -> imagem estática para ser plotado com st.plotly_chart
    """
    st.markdown('##### Average and std delivery time by {}'.format(groupby))
    # Tempo médio e desvio padrão por cidade
    cols = groupby + ['Time_taken(min)']
    df_aux = df1.loc[:,cols].groupby(groupby).agg({'Time_taken(min)':['mean','std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = px.bar(df_aux, x=groupby[0], y='avg_time', error_y='std_time', barmode = 'group', color=color)
   
    return fig