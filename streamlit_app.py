# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose your own fruits you want in your custom smoothie!
    """
)
name_on_order = st.text_input('Name on the order:')
st.write ("The name on your smoothie would be:", name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'), col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
#st.stop()
ingredients_list = st.multiselect ('Choose upto 5 ingredients:', my_dataframe,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    #ingredient_string = ' '
    for fruit_chosen in ingredients_list:
        ingredient_string += fruit_chosen + ' '
        st.write(fruit_chosen)
        st.write(ingredient_string)
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #search_on=pd_df.loc[pd_df['fruit_name'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('"""+ingredient_string+"""','""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    st.stop()
    time_to_insert =  st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

