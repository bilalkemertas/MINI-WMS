import pandas as pd
from database import read_table, write_table


def get_stock():
    return read_table("stok")


def add_stock(kod, isim, adres, miktar, durum):
    df = read_table("stok")

    if not df.empty:
        mask = (df["kod"] == kod) & (df["adres"] == adres)
        if mask.any():
            df.loc[mask, "miktar"] += miktar
        else:
            df = pd.concat([df, pd.DataFrame([{
                "kod": kod,
                "isim": isim,
                "adres": adres,
                "miktar": miktar,
                "durum": durum
            }])], ignore_index=True)
    else:
        df = pd.DataFrame([{
            "kod": kod,
            "isim": isim,
            "adres": adres,
            "miktar": miktar,
            "durum": durum
        }])

    write_table("stok", df)


def remove_stock(kod, adres, miktar):
    df = read_table("stok")

    mask = (df["kod"] == kod) & (df["adres"] == adres)

    if not mask.any():
        return False, "Stok bulunamadı"

    mevcut = df.loc[mask, "miktar"].values[0]

    if mevcut - miktar < 0:
        return False, "NEGATİF STOK ENGELLENDİ"

    df.loc[mask, "miktar"] -= miktar

    write_table("stok", df)
    return True, "OK"


def transfer_stock(kod, src, dst, miktar, isim, durum):
    ok, msg = remove_stock(kod, src, miktar)
    if not ok:
        return False, msg

    add_stock(kod, isim, dst, miktar, durum)
    return True, "TRANSFER OK"
