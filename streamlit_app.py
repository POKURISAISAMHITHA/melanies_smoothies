# Import python packages

import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise your smoothie :cup_with_straw:")
st.write(
    """   Choose the fruits you want in your custom smoothie!
    """
)



Name_on_order = st.text_input('Name_on_smoothie:')
st.write('The name on smoothie will be:',Name_on_order )



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)


cnx= st.connection("snowflake")
session = cnx.session()

ingredients_list =st.multiselect(
'Choose up to 5 ingredients:'
,my_dataframe
,max_selections=5)

if ingredients_list:
    
    ingredients_string =''
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
        st. subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon"+fruit_chosen)
        sf_df =(st.dataframe(data=smoothiefroot_response.json(), use_container_width=True))

    #st.write(ingredients_string) 

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + Name_on_order + """"')"""
    #st.write(my_insert_stmt)
    #st.stop()
    
    #st.write(my_insert_stmt)
    time_to_insert =st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests

