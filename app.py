import streamlit as st
import anasayfa
import modul_sayim
import modul_stok
import modul_uretim
import modul_rapor

# ---------------- INIT ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"


# ---------------- LOGIN ----------------
def login():
    st.title("Login")

    users = st.secrets["users"]

    username = st.text_input("Kullanıcı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş"):
        if username in users and users[username] == password:
            st.session_state.user = username
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Hatalı giriş")


# ---------------- ROUTER ----------------
def router():
    if st.session_state.page == "login":
        login()

    elif st.session_state.page == "home":
        ana_sayfa.goster()

    elif st.session_state.page == "sayim":
        modul_sayim.goster()

    elif st.session_state.page == "stok":
        modul_stok.goster()

    elif st.session_state.page == "uretim":
        modul_uretim.goster()

    elif st.session_state.page == "rapor":
        modul_rapor.goster()


router()
