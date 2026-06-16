# veritabani.py
# (ESKİ FONKSİYONLAR BOZULMADI, SADECE YÖNLENDİRME YAPILDI)

from data_layer import DataLayer

db = DataLayer()

# --- ESKİ KULLANIM UYUMLU KALDI ---
def stok_getir():
    return db.get_stock()

def stok_ekle(item):
    db.add_stock(item)

def hareket_ekle(movement):
    db.add_movement(movement)

def hareket_listele():
    return db.get_movements()
