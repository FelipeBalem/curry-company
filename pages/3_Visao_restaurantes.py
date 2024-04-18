import streamlit as st

from utils import utils
from utils.sidebar import curry_sidebar


st.set_page_config(page_title= 'Visão Restautantes', layout = 'wide')

#Lendo o arquivo
df = utils.read_df()
df1 = df.copy()

#Utilze df_raw quando não quiser que o df seja afetado por filtros
df_raw = df.copy()

#Criando a coluna Week of Year
utils.create_column_week_of_year(df1)

#Inserindo a sidebar e ativando filtros
df1 = curry_sidebar(df1, filter=True)

#--------------------------------------------
# BODY
#--------------------------------------------

# INTRO
st.markdown('# MARKETPLACE - Restaurants View')
st.markdown('## Complete DataFrame Visualization')
st.dataframe(df1)

tab1, tab2 = st.tabs(['Visão Gerencial', '-'])

with tab1:
    st.title('Overall Metrics')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        #Unique delivery
        delivery_men_count = df1.loc[:,'Delivery_person_ID'].nunique()
        col1.metric('Delivery men registered: ', delivery_men_count)

    with col2:
        #distancia média entre restaurante e clientes
         col2.metric( 'Average distance Rest to Client (km): ', utils.avg_distance_restaurant_client(df1) )

    with col3:
        #Tempo médio de entrega durante festival
        col3.metric('Avg delivery time during Festival: ', utils.avg_time_delivery_festival(df1, festival = True))

    with col4:
        #Tempo médio de entrega sem festival
        col4.metric('Avg delivery time without Festival: ', utils.avg_time_delivery_festival(df1, festival = False))
    st.markdown("""---""")

    with st.container():
        col1, col2 = st.columns(2, gap='large')
        with col1:
            #Tempo médio por Cidade
            fig = utils.avg_std_time_delivery_group_by(df1, groupby=['City'])
            st.plotly_chart(fig)

        with col2:
            fig = utils.avg_std_time_delivery_group_by(df1, groupby=['City', 'Road_traffic_density'], color = 'Road_traffic_density')
            st.plotly_chart(fig)  
            
