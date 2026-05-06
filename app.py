import streamlit as st

# INIT
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"


# -------------------------
# LOGIN
# -------------------------
def login():
    st.title("Login")

    users = st.secrets["users"]

    username = st.text_input("User")
    password = st.text_input("Pass", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.user = username
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Hatalı giriş")


# -------------------------
# HOME
# -------------------------
def home():
    st.title("WMS Home")
    st.write(f"User: {st.session_state.user}")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()


# -------------------------
# ROUTER
# -------------------------
if st.session_state.page == "login":
    login()

elif st.session_state.page == "home":
    home()
