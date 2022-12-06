import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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
try:
  #Text entry box
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
      #Fruitvice API response
      fruityvice_response = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice).json()
      fruityvice_normalized = pandas.json_normalize(fruityvice_response)
      # Display as a table
      streamlit.dataframe(fruityvice_normalized)
      
except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# User allowed to add fruit to list
fruit_chosen = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
streamlit.write('Thanks for adding', fruit_chosen)

# Insert fruit into dataframe 
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
