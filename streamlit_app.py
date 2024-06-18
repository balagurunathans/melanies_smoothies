# Import python packages
import streamlit as st

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
my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect ('Choose upto 5 ingredients:', my_dataframe,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredient_string = ' '
    for fruit_chosen in ingredients_list:
        ingredient_string += fruit_chosen + ' '
    #st.write(ingredient_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert =  st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

