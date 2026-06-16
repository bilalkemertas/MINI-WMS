import streamlit as st
from supabase_client import supabase

st.title("WMS TEST PANEL")

# ürün ekleme
urun = st.text_input("Ürün adı")

if st.button("Kaydet"):
    supabase.table("products").insert({
        "name": urun,
        "unit": "adet"
    }).execute()
    st.success("Kaydedildi")

# listele
data = supabase.table("products").select("*").execute()

st.write(data.data)
