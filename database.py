import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "wms.db"


def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stok (
        kod TEXT,
        isim TEXT,
        adres TEXT,
        miktar REAL,
        durum TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hareketler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarih TEXT,
        islem TEXT,
        kod TEXT,
        isim TEXT,
        adres TEXT,
        miktar REAL,
        user TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    cur.execute("INSERT OR IGNORE INTO users VALUES ('admin','1234')")

    conn.commit()
    conn.close()


def read_table(table):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


def write_table(table, df):
    conn = get_conn()
    df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()


def insert_row(table, row: dict):
    conn = get_conn()
    cols = ",".join(row.keys())
    vals = tuple(row.values())
    q = f"INSERT INTO {table} ({cols}) VALUES ({','.join(['?']*len(row))})"
    conn.execute(q, vals)
    conn.commit()
    conn.close()
