import streamlit as st
from database import init_db, read_table
from core.stock_service import add_stock
from core.movement_service import giris, cikis, transfer

init_db()

if "user" not in st.session_state:
    st.session_state.user = None


# LOGIN
if st.session_state.user is None:
    st.title("MINI WMS")

    u = st.text_input("User")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Hatalı")

else:
    st.sidebar.write(f"User: {st.session_state.user}")

    menu = st.sidebar.radio("Menu", ["Stok", "Giriş", "Çıkış", "Transfer", "Rapor"])

    # STOK
    if menu == "Stok":
        st.header("STOK")

        df = read_table("stok")
        st.dataframe(df, use_container_width=True)

        kod = st.text_input("Kod")
        isim = st.text_input("İsim")
        adres = st.text_input("Adres")
        miktar = st.number_input("Miktar", min_value=0.0)

        if st.button("Ekle"):
            add_stock(kod, isim, adres, miktar, "Kullanılabilir")
            st.rerun()

    # GİRİŞ
    elif menu == "Giriş":
        st.header("GİRİŞ")

        kod = st.text_input("Kod")
        isim = st.text_input("İsim")
        adres = st.text_input("Adres")
        miktar = st.number_input("Miktar", min_value=0.0)

        if st.button("Kaydet"):
            giris(kod, isim, adres, miktar, st.session_state.user)
            st.success("OK")

    # ÇIKIŞ
    elif menu == "Çıkış":
        st.header("ÇIKIŞ")

        kod = st.text_input("Kod")
        adres = st.text_input("Adres")
        miktar = st.number_input("Miktar", min_value=0.0)

        if st.button("Çıkış Yap"):
            ok, msg = cikis(kod, adres, miktar, st.session_state.user)
            st.write(msg)

    # TRANSFER
    elif menu == "Transfer":
        st.header("TRANSFER")

        kod = st.text_input("Kod")
        isim = st.text_input("İsim")
        src = st.text_input("Kaynak")
        dst = st.text_input("Hedef")
        miktar = st.number_input("Miktar", min_value=0.0)

        if st.button("Transfer"):
            ok, msg = transfer(kod, isim, src, dst, miktar, st.session_state.user)
            st.write(msg)

    # RAPOR
    elif menu == "Rapor":
        st.header("RAPOR")

        df = read_table("hareketler")
        st.dataframe(df, use_container_width=True)
