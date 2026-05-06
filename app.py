import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================
# DATABASE (SQLite)
# =========================
DB_NAME = "wms.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    # USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # STOK
    c.execute("""
    CREATE TABLE IF NOT EXISTS stok (
        kod TEXT,
        isim TEXT,
        adres TEXT,
        miktar REAL,
        durum TEXT
    )
    """)

    # HAREKETLER
    c.execute("""
    CREATE TABLE IF NOT EXISTS hareketler (
        tarih TEXT,
        islem TEXT,
        kod TEXT,
        isim TEXT,
        adres TEXT,
        miktar REAL,
        user TEXT
    )
    """)

    # default admin
    c.execute("INSERT OR IGNORE INTO users VALUES ('admin','1234')")

    conn.commit()
    conn.close()

# =========================
# DB HELPERS
# =========================
def read_table(table):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

def write_table(table, df):
    conn = get_conn()
    df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

# =========================
# INIT
# =========================
init_db()

# =========================
# LOGIN
# =========================
def login():
    st.title("📦 MINI WMS LOGIN")

    u = st.text_input("User")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        res = cur.fetchone()
        conn.close()

        if res:
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Hatalı giriş")

# =========================
# STOK PAGE
# =========================
def stok_page():
    st.header("📦 STOK")

    df = read_table("stok")

    st.dataframe(df, use_container_width=True)

    st.subheader("Yeni Stok")

    kod = st.text_input("Kod")
    isim = st.text_input("İsim")
    adres = st.text_input("Adres")
    miktar = st.number_input("Miktar", min_value=0.0)
    durum = st.selectbox("Durum", ["Kullanılabilir", "Blokeli"])

    if st.button("Ekle"):
        new = pd.DataFrame([{
            "kod": kod,
            "isim": isim,
            "adres": adres,
            "miktar": miktar,
            "durum": durum
        }])

        df = pd.concat([df, new], ignore_index=True)
        write_table("stok", df)

        st.success("Eklendi")
        st.rerun()

# =========================
# HAREKET PAGE
# =========================
def hareket_page():
    st.header("🔁 HAREKET")

    df = read_table("hareketler")
    st.dataframe(df, use_container_width=True)

    st.subheader("Yeni Hareket")

    islem = st.selectbox("İşlem", ["GİRİŞ", "ÇIKIŞ"])
    kod = st.text_input("Kod")
    miktar = st.number_input("Miktar", min_value=0.0)

    if st.button("İşle"):
        stok = read_table("stok")

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        if islem == "GİRİŞ":
            if not stok.empty and kod in stok["kod"].values:
                stok.loc[stok["kod"] == kod, "miktar"] += miktar
            else:
                stok = pd.concat([stok, pd.DataFrame([{
                    "kod": kod,
                    "isim": "-",
                    "adres": "-",
                    "miktar": miktar,
                    "durum": "Kullanılabilir"
                }])])

        elif islem == "ÇIKIŞ":
            if kod in stok["kod"].values:
                mevcut = stok.loc[stok["kod"] == kod, "miktar"].values[0]
                if mevcut - miktar < 0:
                    st.error("Negatif stok olamaz")
                    return
                stok.loc[stok["kod"] == kod, "miktar"] -= miktar

        # log
        hareket = pd.DataFrame([{
            "tarih": now,
            "islem": islem,
            "kod": kod,
            "isim": "-",
            "adres": "-",
            "miktar": miktar,
            "user": st.session_state.user
        }])

        df_h = read_table("hareketler")
        df_h = pd.concat([df_h, hareket], ignore_index=True)

        write_table("stok", stok)
        write_table("hareketler", df_h)

        st.success("OK")
        st.rerun()

# =========================
# MAIN APP
# =========================
if st.session_state.user is None:
    login()
else:
    st.sidebar.write(f"User: {st.session_state.user}")

    menu = st.sidebar.radio("Menu", ["Stok", "Hareket"])

    if menu == "Stok":
        stok_page()
    elif menu == "Hareket":
        hareket_page()
