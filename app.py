import streamlit as st
from PIL import Image

import image_analysis
from image_analysis import *

if __name__ == '__main__':
    st.set_page_config(page_title='Azure', page_icon=":checkered_flag:")
    st.title("Projet Azure")

    option = st.selectbox('Rechercher un tag', ('Email', 'Home phone', 'Mobile phone'))

    img_file = st.file_uploader("Ajouter une image", type=['png', 'jpeg', 'jpg'])
    if img_file is not None:
        st.image(img_file)
        img = Image.open(img_file)
        print(get_tags_from_image(img))
        image_analysis.get_tags_from_image(img)

