import streamlit as st
from uas_aw import show_aw_dashboard
from uas_imdb import show_imdb_dashboard

# Judul dan deskripsi aplikasi
st.sidebar.title('WELCOME TO DASHBOARD DATA VISUALISASI')
st.sidebar.write('by Khoirunisa 21082010089')
st.sidebar.markdown("""
    <div style="text-align: justify;">
    <p>Selamat datang di dashboard by Khoirunisa! 
    Silakan pilih opsi di sidebar untuk menampilkan dashboard Adventure Works atau IMDb.</p>
    </div>
""",unsafe_allow_html=True)



# Pilihan sidebar untuk memilih dashboard
dashboard_option = st.sidebar.selectbox('Pilih Dashboard:', ('Adventure Works', 'IMDb'))

# Tampilkan dashboard sesuai pilihan pengguna
if dashboard_option == 'Adventure Works':
    show_aw_dashboard()
elif dashboard_option == 'IMDb':
    show_imdb_dashboard()