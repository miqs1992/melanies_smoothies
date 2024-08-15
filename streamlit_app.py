# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name = st.text_input('Name on Smoothie')
st.write('Name on your Smoothie will be: ', name)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredient_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)
if ingredient_list:
    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name + """')"""

    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!, ' + name + '!')
      
