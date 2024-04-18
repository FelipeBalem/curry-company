from PIL import Image
import streamlit as st
from datetime import datetime
#----------------------------------
#MENU LATERAL
#----------------------------------
def curry_sidebar(df1, filter=True):#Ativando filtros
    """
    Create a common sidebar with input widgets to filter the information of curry_company
    dataframe.

    INPUT: df1 -> curry_company dataframe after 
           filter -> Boolean, activate the filter options

    OUTPUT: if filter = True, returns df1 with filter aplication
    """

    df_raw = df1.copy()

    #Cabeçalho do menu lateral
    logo_path = 'images/curry-company-logo.jpeg'
    logo = Image.open( logo_path )
    st.sidebar.image(logo, width=120)
    
    st.sidebar.markdown("# Curry Company")
    st.sidebar.markdown("## The fastest delivery")
    st.sidebar.markdown("""---""")

    if filter:
        #Data Slider
        
        max_date = datetime(2022, 4, 13)
        min_date = datetime(2022, 2, 11)
        
        date_slider = st.sidebar.slider(
            label = 'Choose a date limit',
            min_value = min_date,
            max_value = max_date,
            value = max_date,
            format='YYYY-MM-DD')
        
        
        st.sidebar.markdown("""---""")
        
        # Nível do tráfego
        list_of_options = df1['Road_traffic_density'].unique()
        
        traffic_options = st.sidebar.multiselect(
            label = 'Select traffic conditions',
            options = list_of_options,
            default = list_of_options )
        
        
        #Idade dos entregadores
        min_age = df1.loc[:,'Delivery_person_Age'].min()
        max_age = df1.loc[:,'Delivery_person_Age'].max()
        
        start_age, end_age = st.sidebar.select_slider(
            label='Choose the Delivery Men Age range:',
            options= range(min_age,max_age+1),
            value = (min_age, max_age)
        )
        
        # Notas dos entregadores
        min_rate = int(round(df1.loc[:,'Delivery_person_Ratings'].min()))
        max_rate = int(round(df1.loc[:,'Delivery_person_Ratings'].max()))
        
        start_rate, end_rate = st.sidebar.select_slider(
            label='Choose the Delivery Men Ratings range:',
            options= range(min_rate,max_rate+1),
            value = (min_rate, max_rate)
        )
        
        #Condições do tempo
        list_of_weathers = df1['Weatherconditions'].unique()
        
        weather_options = st.sidebar.multiselect(
            label = 'Select weather conditions',
            options = list_of_weathers,
            default = list_of_weathers)
        
        #Tipo de veículo
        list_of_vehicle = df1['Type_of_vehicle'].unique()
        
        vehicle_options = st.sidebar.multiselect(
            label = 'Select Type of Vehicle',
            options = list_of_vehicle,
            default = list_of_vehicle)
        
        #Multiple deliveries
        multiple_deliveries = st.sidebar.radio(
            label = ' One or Multiple Deliveries?',
            options= ['Both', 'One Delivery', 'Multiple Delivery'],
            index = 0 )
        
        # Festival
        festival = st.sidebar.radio(
            label = 'I/O Festival?',
            options = ['Both', 'Festival', 'No Festival'],
            index = 0 )
        
        # City
        list_of_city = df1['City'].unique()
        
        city_options = st.sidebar.multiselect(
            label = 'Select Type of City',
            options = list_of_city,
            default = list_of_city)
        
        #Time Taken
        min_time = df1.loc[:,'Time_taken(min)'].min()
        max_time = df1.loc[:,'Time_taken(min)'].max()
        
        start_time, end_time = st.sidebar.select_slider(
            label='Choose the Delivery Timing range:',
            options= range(min_time,max_time+1),
            value = (min_time, max_time)
        )
        
        #Week_of_year
        min_week = df1.loc[:,'Week_of_year'].min()
        max_week = df1.loc[:,'Week_of_year'].max()
        
        start_week, end_week = st.sidebar.select_slider(
            label='Choose the Week of Year range:',
            options= range(min_week,max_week+1),
            value = (min_week, max_week)
        )
    
        #
        #---------------------------------------------
        #FILTERING DATAFRAME
        #---------------------------------------------
    
    
            
        # by Traffic
        selected_lines = df1.loc[:,'Road_traffic_density'].isin(traffic_options)
        df1 = df1.loc[selected_lines, :].copy()
    
        
        # by Date
        selected_lines = df1.loc[:, 'Order_Date'] <= date_slider
        df1 = df1.loc[selected_lines, :].copy()
    
        
        # by Age
        selected_lines = ((df1.loc[:, 'Delivery_person_Age'] >= start_age) & (df1.loc[:, 'Delivery_person_Age'] <= end_age))
        df1 = df1.loc[selected_lines, :].copy()
    
        
        # by rating
        selected_lines = ((df1.loc[:, 'Delivery_person_Ratings'] >= start_rate) & (df1.loc[:, 'Delivery_person_Ratings'] <= end_rate))
        df1 = df1.loc[selected_lines, :].copy()
    
        
        # by weatherconditions
        selected_lines = df1.loc[:,'Weatherconditions'].isin(weather_options)
        df1 = df1.loc[selected_lines, :].copy()
    
        
        #by Type_of_vehicle
        selected_lines = df1.loc[:,'Type_of_vehicle'].isin(vehicle_options)
        df1 = df1.loc[selected_lines, :].copy()
    
        
        #by Multiple_deliveries
        if multiple_deliveries == 'Multiple Delivery':
            selected_lines = df1.loc[:, 'multiple_deliveries'] == True
        elif multiple_deliveries == 'One Delivery':
            selected_lines = df1.loc[:, 'multiple_deliveries'] == False
        else:
            selected_lines = ((df1.loc[:, 'multiple_deliveries'] == True) | (df1.loc[:, 'multiple_deliveries'] == False))
            
        df1 = df1.loc[selected_lines, :].copy()
    
        
        # by Festival
        if festival == 'Festival':
            selected_lines = df1.loc[:, 'Festival'] == True
            
        elif festival == 'No Festival':
            selected_lines = df1.loc[:, 'Festival'] == False
            
        else:
            selected_lines = ((df1.loc[:, 'Festival'] == True) | (df1.loc[:, 'Festival'] == False))
        
        df1 = df1.loc[selected_lines, :].copy()
        
        
        #by City
        selected_lines = df1.loc[:,'City'].isin(city_options)
        df1 = df1.loc[selected_lines, :].copy()
    
        
        #by Time_taken(min)
        selected_lines = ((df1.loc[:, 'Time_taken(min)'] >= start_time) & (df1.loc[:, 'Time_taken(min)'] <= end_time))
        df1 = df1.loc[selected_lines, :].copy()
    
        
        #by Week_of_Year
        selected_lines = ((df1.loc[:, 'Week_of_year'] >= start_week) & (df1.loc[:, 'Week_of_year'] <= end_week))
        df1 = df1.loc[selected_lines, :].copy()

    #Ignorando filtros
        disable_filters = st.toggle(label = 'Desativar filtros', value=False)
        if disable_filters:
            df1 = df_raw.copy()
    
    #Footer
    st.sidebar.markdown("""---""")
    st.sidebar.markdown("### Powered by: Felipe Balem")

    return df1