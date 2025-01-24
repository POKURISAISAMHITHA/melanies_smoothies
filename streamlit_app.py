# Import required libraries
import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import requests

# Streamlit app title and description
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)

# Text input for the smoothie name
Name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on smoothie will be:', Name_on_order)

# Establish Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch available fruit options
fruit_options_df = session.table("smoothies.public.fruit_options").select(col('fruit_name')).to_pandas()

# Convert fruit options to a list for the multiselect widget
fruit_options_list = fruit_options_df['FRUIT_NAME'].tolist()

# Multiselect widget for choosing ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options_list,
    max_selections=5
)

if ingredients_list:
    # Display nutrition information for selected fruits
    ingredients_string = ", ".join(ingredients_list)  # Create a comma-separated string of ingredients
    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")
        # Fetch nutrition information for each fruit
        try:
            api_url = f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}"
            smoothiefroot_response = requests.get(api_url)
            if smoothiefroot_response.status_code == 200:
                st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            else:
                st.warning(f"Could not fetch data for {fruit_chosen}.")
        except Exception as e:
            st.error(f"An error occurred while fetching data for {fruit_chosen}: {e}")

    # Insert order into the database
    my_insert_stmt = (
        "INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (%s, %s)"
    )
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            session.sql(my_insert_stmt, [ingredients_string, Name_on_order]).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred while placing your order: {e}")
