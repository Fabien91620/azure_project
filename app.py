import streamlit as st
from PIL import Image

import image_analysis
from image_analysis import *

if __name__ == '__main__':
    st.set_page_config(page_title='Azure', page_icon=":checkered_flag:")
    st.title("Projet Azure")

    option = st.selectbox('Rechercher un tag', ('Email', 'Home phone', 'Mobile phone'))

    with st.expander("Charger une image"):
        if img_file != None: #is not ne fonctionne pas 
        img_file = st.file_uploader("Ajouter une image", type=['png', 'jpeg', 'jpg', 'webp'])
        st.image(img_file)
        img = Image.open(img_file)

     with st.expander('Déduction de tag'):
        if img != None:
            tags = image_analysis.get_tags_from_image(img)
            if tags !=  None and len(tags) > 0 :
                opt_col1, opt_col2, opt_col3 = st.columns(3)
                for tag in tag: 
                    opt_col2.write(':point_right:     ' + 
                    "'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100) + 
                    '     :point_left:')
        else:
            st.write(":warning: Vous devez avoir chargé une image afin de déduire les tags :warning:")

