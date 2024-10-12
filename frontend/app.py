import streamlit as st
import requests
import pandas as pd

st.title("E-commerce Product Scraper")
product_url = st.text_input("Product Name")

st.subheader("Products List")
res = requests.get("http://127.0.0.1:5000/").json()

df = pd.DataFrame(res)
df_transposed = df.transpose()

if all(col in df_transposed.columns for col in ['id', 'price', 'title']):
    df_final = df_transposed[['title', 'price']]
    st.dataframe(df_final)
else:
    st.error("json data doesn't contain required columns")

st.subheader("Raw JSON Data")
st.json(res)