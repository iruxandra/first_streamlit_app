import streamlit
import snowflake.connector
import pandas as pd
import requests
from urllib.error import URLError


streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭Build Your On Fruit Smoothie🥝🍇')


my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
streamlit.dataframe(my_fruit_list)

#New section to display fruityvice api response
# streamlit.header("Fruityvice Fruit Advice!")
# fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
# streamlit.write('The user entered', fruit_choice)


# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


# #take the json verison of the response and normalise it
# fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

# #output it the screen as a table
# streamlit.dataframe(fruityvice_normalized)


#create a function
def get_fruityvice_data(this_fruit_choice):
  fruitvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#New section to display fruityvice api response

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information.')
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
      

streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)



add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)

#This will not work correctly for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
