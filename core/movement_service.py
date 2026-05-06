from datetime import datetime
import pandas as pd
from database import read_table, write_table, insert_row
from core.stock_service import add_stock, remove_stock


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def giris(kod, isim, adres, miktar, user):
    add_stock(kod, isim, adres, miktar, "Kullanılabilir")

    insert_row("hareketler", {
        "tarih": now(),
        "islem": "GİRİŞ",
        "kod": kod,
        "isim": isim,
        "adres": adres,
        "miktar": miktar,
        "user": user
    })

    return True


def cikis(kod, adres, miktar, user):
    ok, msg = remove_stock(kod, adres, miktar)

    if not ok:
        return False, msg

    insert_row("hareketler", {
        "tarih": now(),
        "islem": "ÇIKIŞ",
        "kod": kod,
        "isim": "-",
        "adres": adres,
        "miktar": miktar,
        "user": user
    })

    return True, "OK"


def transfer(kod, isim, src, dst, miktar, user):
    ok, msg = remove_stock(kod, src, miktar)

    if not ok:
        return False, msg

    add_stock(kod, isim, dst, miktar, "Kullanılabilir")

    insert_row("hareketler", {
        "tarih": now(),
        "islem": "TRANSFER",
        "kod": kod,
        "isim": isim,
        "adres": f"{src}->{dst}",
        "miktar": miktar,
        "user": user
    })

    return True, "OK"
