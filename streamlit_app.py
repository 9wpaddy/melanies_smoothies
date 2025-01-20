# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie!"""
)

name_of_order  =st.text_input('Name on Smoothie:')
st.write('Name on your Smoothie will be: ',name_of_order)
cnx =st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe
    ,max_selections =5
   
)



if ingredients_list :
   
    ingredients_string =''
    for friut_chosen  in ingredients_list:
        ingredients_string+=friut_chosen + ' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_of_order+"""')"""
   # st.write(my_insert_stmt)
    

    time_to_insert=st.button('Submit Order')
    
    #if ingredients_string :
    
    if time_to_insert :
        session.sql(my_insert_stmt).collect()
        st.success("Your smoothie is ordered, " + name_of_order +"!", icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


    
    
