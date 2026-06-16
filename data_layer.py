import streamlit as st

# --- SAF VERİ KATMANI (ABSTRACTION LAYER) ---

class DataLayer:
    def __init__(self):
        # fallback mode (şimdilik gspread devre dışı)
        self.mode = "local"

    # ---------------- STOCK ----------------
    def get_stock(self):
        """
        Mevcut stokları döndürür
        """
        if self.mode == "local":
            return st.session_state.get("stock_data", [])
        return []

    def add_stock(self, item):
        """
        Stok ekleme
        """
        if "stock_data" not in st.session_state:
            st.session_state["stock_data"] = []

        st.session_state["stock_data"].append(item)

    # ---------------- MOVEMENTS ----------------
    def add_movement(self, movement):
        if "movements" not in st.session_state:
            st.session_state["movements"] = []

        st.session_state["movements"].append(movement)

    def get_movements(self):
        return st.session_state.get("movements", [])
