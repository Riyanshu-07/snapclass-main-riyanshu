import streamlit as st  


def style_background_home():
    st.set_page_config(page_title="SNAP CLASS", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #5865F2 !important;
            
        }
        .stApp div[data-testid="stColumn"]{
          background: white;
          border-radius: 40px;
          padding: 1.5rem;
          min-height: 320px;
          max-width: 420px;
          margin: auto;
          color: black;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
def style_background_dashboard():
    st.set_page_config(page_title="SNAP CLASS", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #E0E3FF !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
    

def base_layout():
    st.set_page_config(page_title="SNAP CLASS", layout="wide")
    st.markdown(
        """
        
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
              #MainMenu,header,footer{
                visibility:hidden !important;
              }
              .block-container {
                  padding-top: 1rem !important;
               
              }
              h1{
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height:1.1rem !improtant;
                margin-bottom: 0rem !important;

              }

              h2{
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 1.5rem !important;
                line-height:1.1rem !improtant;
                margin-bottom: 0rem !important;
              }
              h3,h4,p,{
                font-family: 'Outfit', sans-serif !important;
              }
              button{
                border-radius: 1.5rem !important;
                background-color: black  !important;
                color:white !important;
                padding: 10px 20px !important;
                border:None !important;
                transition: transform 0.3s ease-in-out !important;
              }

              button[kind="secondary"]{
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color:white !important;
                padding: 10px 20px !important;
                border:None !important;
                transition: transform 0.3s ease-in-out !important;
              }
              button[kind="tertiary"]{
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color:white !important;
                padding: 10px 20px !important;
                border:None !important;
                transition: transform 0.3s ease-in-out !important;
              }
              button:hover{
                    transform: scale(1.05) !important;
              }

        </style>
        """,
        unsafe_allow_html=True,
    )
    
    