# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Orders! :cup_with_straw:")
st.write(
    """Orders that needs to be filled
    """
)
#name_on_order = st.text_input('Name on the order:')
#st.write ("The name on your smoothie would be:", name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    time_to_insert =  st.button('Submit')
    if time_to_insert:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                     , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success('Your Smoothie is ordered!', icon="✅")
        except:
            st.write('Something went wrong!')
else:
    st.success('No Pending Orders!', icon="✅")
