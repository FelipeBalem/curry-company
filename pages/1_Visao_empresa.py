import streamlit as st

from utils import utils
from utils.sidebar import curry_sidebar

st.set_page_config(page_title= 'Visão Empresa', layout = 'wide')

#Lendo o arquivo
df = utils.read_df()
df1 = df.copy()

#Utilze df_raw quando não quiser que o df seja afetado por filtros
df_raw = df.copy()

#Criando a coluna Week of Year
utils.create_column_week_of_year(df1)


#Inserindo a sidebar e ativando filtros
df1 = curry_sidebar(df1, filter=True)


#Visão empresa


#-----------------------------------
#BODY
#-----------------------------------


# INTRO
st.markdown('## Complete DataFrame Visualization')
st.dataframe(df1.loc[:, :])


#FAZENDO TABS PARA DISTRIBUIR OS GRÁFICOS
# Para plotar gráficos, utilizar o comando st.plotly_chart(imagem do gráfico, use_container_width=True)
tab1, tab2, tab3 = st.tabs(['Management view', 'Tactical view', 'Geographic view'])

with tab1:
     #VISÃO GERENCIAL
    with st.container():        
        #Gráfico Qnt de pedidos por dia
        utils.deliveries_by_bar(df1, 'Order_Date')
        st.markdown("""---""")
        
    with st.container():
        col1, col2 = st.columns(2)

        with col1:          
            #Gŕafico qnt pedidos por tipo de tráfego           
            utils.deliveries_by_pie(df1, 'Weatherconditions')

        with col2:
            # Gŕafico de tipo de cidade e densidade de tráfego
            utils.deliveries_by_bar_group(df1, ['City', 'Road_traffic_density'])

    with st.container(): 
        #Entregas por tipo de tráfego 
        utils.deliveries_by_bar_group(df1, ['Order_Date', 'Road_traffic_density'])

#Tatical View
with tab2:
    
    with st.container():
    #Média de entrega por entregador por semana
        utils.avg_delivery_per_week_by(df1, 'Delivery_person_ID')
        

    with st.container():
        #Quantidade de pedidos por semana
        st.markdown("""---""")
        utils.number_of_deliveries_per(df1, 'Week_of_year')
        
with tab3:
    #VISÃO GEOGRÁFICA
    with st.container():
        utils.restaurants_map(df1, groupby=['City','Road_traffic_density'])
        
  