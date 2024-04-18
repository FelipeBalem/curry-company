
import pandas as pd

import streamlit as st

from utils import utils
from utils.sidebar import curry_sidebar

#--------------------------------------
# TRATANDO O ARQUIVO
#-------------------------------------

#======================================
# STREAMLIT
#=======================================
#streamlit run nome-arquivo.py
#Lendo o arquivo


df = utils.read_df()
df1 = df.copy()

#Utilze df_raw quando não quiser que o df seja afetado por filtros
df_raw = df.copy()

#Criando a coluna Week of Year
utils.create_column_week_of_year(df1)

#Trocando vehicle conditions de 0,1,2 para ruim, regular, ótimo
utils.replace_vehicle_conditions(df1)

#Mudando o layout da página para WIDE
st.set_page_config(page_title= 'Curry Company - Home', layout = 'wide')

#Inserindo a sidebar e ativando filtros
df1 = curry_sidebar(df1, filter=True)

#--------------------------------------------
# BODY
#--------------------------------------------



# INTRO
st.markdown('# MARKETPLACE - Delivery Men View')
st.markdown('## Complete DataFrame Visualization')
st.dataframe(df1.loc[:, :])

tab1, tab2 = st.tabs(['Visão Gerencial', '-'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
 

        col1, col2 = st.columns(2, gap = 'large')
        
        with st.container():
            #IDADE
            with st.container():
                st.title('Age Metrics*')                
                
                max_value = utils.find_max_value(df1, column = 'Delivery_person_Age')
                min_value = utils.find_min_value(df1, column = 'Delivery_person_Age')
                avg_value = utils.find_mean_value(df1, column = 'Delivery_person_Age')
                
                s_col1, s_col2, s_col3= st.columns(3, gap = 'small')
                with s_col1:
                    s_col1.metric('OLDER: ', max_value)
                with s_col2:
                    s_col2.metric('NEWER: ', min_value)

                with s_col3: 
                    s_col3.metric('AVERAGE: ', round(avg_value))
           
            st.markdown("""---""")
            
        with st.container():
            st.title('Delivery Metrics')
            
            avg_deliveries_by = utils.avg_deliveries_by(df1, 'Delivery_person_ID')
                
            st.metric('Deliveries / Delivery Man: ', round(avg_deliveries_by))
            
            s_col4, s_col5 = st.columns(2, gap='large')
            
            with s_col4:
                #10 mais rápidos
                top_10 = utils.top_10_delivery_men_by(df1, 'City')
               
                st.dataframe(top_10, use_container_width=True)

            with s_col5:
                #10 mais lentos
                last_10 = utils.last_10_delivery_men_by(df1, 'City')
                st.dataframe(last_10, use_container_width=True)
                
    with st.container():
        #AVALIAÇÕES MÉDIA POR 
            avg_rating = utils.avg_rating_by(df1, by='Delivery_person_ID')
        
            st.dataframe(avg_rating, use_container_width=True)
            st.markdown("""---""")
        

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            # GRÁFICO AVALIAÇÃO MÉDIA POR TRÁFEGO
            df_avg_ratings_per_road = utils.plot_avg_rating_by(df1, by = 'Road_traffic_density')
            
            st.bar_chart(df_avg_ratings_per_road, use_container_width=True)

        with col2:
            #AVALIAÇÃO MÉDIA POR CLIMA
            df_avg_ratings_per_weather = utils.plot_avg_rating_by(df1, by = 'Weatherconditions')

            st.bar_chart(df_avg_ratings_per_weather, use_container_width=True)

    with st.container():
        #CONDIÇÕES DO VEÍCULO
        
        df_vehicle_conditions = utils.deliveries_by_pie(df1, by='Vehicle_condition')