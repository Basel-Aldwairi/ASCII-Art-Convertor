import streamlit as st

# import ASCII_gen


st.title('ASCII Convertor')


custom_image = st.toggle('Use Custom Image')



if custom_image:
    web = st.toggle('File or Web')

    if web:
        url = st.text_input('Enter URL')

    else:
        path = st.text_input('Enter Path')


