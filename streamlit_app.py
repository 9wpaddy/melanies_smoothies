# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!"""
)

name_of_order  =st.text_input('Name on Smoothie:')
st.write('Name on your Smoothie will be: ',name_of_order)
cnx =st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df =my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

# Convert snowflake frame to Pandas Dataframe so we can use LOC function 
ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe
    ,max_selections =5
   
)

if ingredients_list :
    ingredients_string =''
    for fruit_chosen  in ingredients_list:
        ingredients_string+=fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        #st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)  
    
