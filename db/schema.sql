CREATE TABLE IF NOT EXISTS stok (
    kod TEXT,
    isim TEXT,
    adres TEXT,
    miktar REAL,
    durum TEXT
);

CREATE TABLE IF NOT EXISTS hareketler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarih TEXT,
    islem TEXT,
    kod TEXT,
    isim TEXT,
    adres TEXT,
    miktar REAL,
    user TEXT
);

CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
);
