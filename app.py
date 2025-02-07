import streamlit as st
import pickle
from model import HybridRecommendation,ContentBasedRecomendation,Collaborative_Fitering
import base64

def add_bg_from_local(image_file): # Them background vao website
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(

    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
#add_bg_from_local('data/background.jpg')


st.markdown("<h2 style='font-size: 30px; color: white;'> 📚 Book Recommendation System </h2>", unsafe_allow_html=True)



with open("data/title.pkl", "rb") as f:
    title_book = pickle.load(f)

# Load model đã lưu
with open('model/hybrid_model.pkl', 'rb') as f:
    model = pickle.load(f)

selected_book = st.selectbox('🔍 Type or Select a book', title_book)



if st.button('🔄 Show Recommendation'):

    recommendation = model.recomend(selected_book)

    st.markdown("<h2 style='font-size: 18px; color: white;'> 🔍 Selected Book</h2>", unsafe_allow_html=True)


    if len(recommendation) < 5:
        st.error("Không đủ dữ liệu để gợi ý 5 sách.")
    else:
        books = [(title, img_url) for title, img_url in recommendation]

        col_1, _, _, _, _ = st.columns(5)
        with col_1:
            st.image(books[0][1], caption=books[0][0],width=100)  

        st.markdown("<h2 style='font-size: 18px; color: white;'>🔥 Top Books for You 🔥</h2>", unsafe_allow_html=True)


        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for col, (title, img_url) in zip(cols, books[1:]):
            with col:
                st.image(img_url, caption=title, width=100)

        
