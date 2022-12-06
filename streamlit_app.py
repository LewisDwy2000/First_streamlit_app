import streamlit
import pandas
import requests
import snowflake.connector

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

streamlit.title('My Parents Now Healthy Diner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.Fruit), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[my_fruit_list['Fruit'].isin(fruits_selected)]

# Display data 
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')

#Text entry box
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

#Fruitvice API response
fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice).json()

fruityvice_normalized = pandas.json_normalize(fruityvice_response)
# Display as a table
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur_execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)
