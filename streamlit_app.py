# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customise your smoothie :cup_with_straw:")
st.write(
    """   Choose the fruits you want in your custom smoothie!
    """
)



Name_on_order = st.text_input('Name_on_smoothie:')
st.write('The name on smoothie will be:',Name_on_order )
cnx =st.connection("snowflake")
session =cnx.session()



my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()

ingredients_list =st.multiselect(
'Choose up to 5 ingredients:'
,my_dataframe)
ingredients_string="
if ingredients_list:
    
    ingredients_string =""
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ""
        search_on =pd_df[pd_df['FRUIT_NAME']==fruit_chosen,'SEARCH_ON'].iloc[0]

        st.subheader(fruit_chosen+'nutrition information')

        smoothiefroot_response = requests.get(
            "https://fruityvice.com/api/fruit/" + search_on
        )
        sf_df = st.dataframe(
            data=smoothiefroot_response.json(), use_container_width=True
        )

    

time_to_insert = st.button('Submit Order')
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('""" + ingredients_string + """','"""+name_on_order+"""') """
if time_to_insert:

    session.sql(my_insert_stmt).collect()

    st.success("Your Smoothie is ordered!", icon="✅")
