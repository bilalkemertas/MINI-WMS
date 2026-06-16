import streamlit as st
modul_sayim.show()

st.set_page_config(page_title="MINI WMS", layout="wide")

st.title("MINI WMS")

menu = st.sidebar.selectbox(
    "Menü",
    ["Sayım", "Stok", "Teslim Alma", "Üretim"]
)

if menu == "Sayım":
    import modul/sayim
    modul/sayim.show()

elif menu == "Stok":
    import modul_stok
    modul_stok.show()

elif menu == "Teslim Alma":
    import modul_teslim_alma
    modul_teslim_alma.show()

elif menu == "Üretim":
    try:
        import modul_uretim
        modul_uretim.show()
    except:
        st.warning("Üretim modülü yok")
