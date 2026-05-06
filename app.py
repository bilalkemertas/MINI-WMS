from database import get_conn

if st.session_state.user is None:
    st.title("MINI WMS LOGIN")

    u = st.text_input("User")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (u, p)
        )

        res = cur.fetchone()
        conn.close()

        if res:
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Hatalı giriş")
