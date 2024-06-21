import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
import plotly.express as px

# Membuat koneksi ke database MySQL
conn = mysql.connector.connect(
    host="kubela.id",
    user="davis2024irwan",
    port=3306,
    password="wh451n9m@ch1n3",
    database="aw"
)

# Fungsi untuk menjalankan query dan mengembalikan DataFrame
def run_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    return pd.DataFrame.from_records(rows, columns=columns)

def show_aw_dashboard():
    st.title('ADVENTURE WORKS')
    st.write("""
    Selamat datang di dashboard Adventure Work by Khoirunisa!
    Dashboard ini menampilkan beberapa visualisasi untuk menganalisis penjualan produk Adventure Work. 
    Nikmati eksplorasi data Anda!
    """)

    # VISUALISASI COMPARISON
    # Query 
    query_sales_by_category = '''
    SELECT 
        t.CalendarYear,
        pc.ProductCategoryKey,
        pc.EnglishProductCategoryName,
        SUM(fs.SalesAmount) AS TotalSales
    FROM 
        FactInternetSales fs
    JOIN 
        DimProduct dp ON fs.ProductKey = dp.ProductKey
    JOIN 
        DimProductSubcategory psc ON dp.ProductSubcategoryKey = psc.ProductSubcategoryKey
    JOIN 
        DimProductCategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
    JOIN 
        DimTime t ON fs.OrderDateKey = t.TimeKey
    GROUP BY 
        t.CalendarYear, pc.ProductCategoryKey
    '''
    st.write('## COMPARISON: Penjualan Produk per Kategori')
    df_sales_by_category = run_query(query_sales_by_category)
    selected_year = st.selectbox('Pilih Tahun:', df_sales_by_category['CalendarYear'].unique())

    # Visualisasi
    filtered_df = df_sales_by_category[df_sales_by_category['CalendarYear'] == selected_year]
    fig = px.bar(
        filtered_df, 
        x='EnglishProductCategoryName', 
        y='TotalSales', 
        color='EnglishProductCategoryName',
        title=f'Perbandingan Penjualan Produk per Kategori untuk Tahun {selected_year}',
        labels={'EnglishProductCategoryName': 'Kategori Produk', 'TotalSales': 'Total Penjualan'},
        hover_data={'TotalSales': ':,.2f'},
        color_discrete_sequence=['#0E46A3', '#1E0342', '#9AC8CD', '#E1F7F5'] 
    )
    st.plotly_chart(fig)

    # Deskripsi
    st.write('#### Deskripsi:')
    st.markdown("""
        <div style="text-align: justify;">
            <p>Visualisasi di atas menggunakan bar chart untuk membandingkan total penjualan produk
            di setiap kategori pada setiap tahun. Filter dropdown menyediakan pilihan sepanjang periode 
            (2001-2004). Pada tahun 2001 dan 2002, hanya terdapat satu produk yang diproduksi, 
            yaitu bike, dengan total penjualan sebesar 3 juta yang mengalami peningkatan dua kali lipat 
            pada tahun berikutnya. Pada tahun 2003, terdapat tiga produk yaitu bike, clothing, dan accessories 
            dengan penjualan tertinggi adalah produk bike dan terendah adalah clothing. Pada tahun 2004, 
            penjualan tertinggi masih tetap bike dan terendah tetap clothing. Dari data ini dapat disimpulkan bahwa 
            produk bike secara konsisten mendominasi penjualan sepanjang periode tersebut, sementara produk clothing 
            memiliki penjualan yang paling rendah. Tren ini menunjukkan pentingnya strategi pemasaran yang lebih efektif 
            untuk kategori clothing agar dapat meningkatkan penjualan, sementara mempertahankan dan meningkatkan penjualan 
            untuk produk bike yang sudah unggul.</p>
        </div>
        """, unsafe_allow_html=True)


    # VISUALISASI COMPOSISION
    # Query untuk mengambil data penjualan berdasarkan subkategori produk
    query_sales_by_subcategory = '''
    SELECT 
        pc.EnglishProductCategoryName,
        psc.EnglishProductSubcategoryName,
        t.CalendarYear,
        SUM(fs.SalesAmount) AS TotalSales
    FROM 
        FactInternetSales fs
    JOIN 
        DimProduct dp ON fs.ProductKey = dp.ProductKey
    JOIN 
        DimProductSubcategory psc ON dp.ProductSubcategoryKey = psc.ProductSubcategoryKey
    JOIN 
        DimProductCategory pc ON psc.ProductCategoryKey = pc.ProductCategoryKey
    JOIN 
        DimTime t ON fs.OrderDateKey = t.TimeKey
    WHERE 
        pc.ProductCategoryKey IN (1, 2, 3)
    GROUP BY 
        pc.EnglishProductCategoryName, psc.EnglishProductSubcategoryName, t.CalendarYear
    ORDER BY 
        t.CalendarYear
    '''

    # Jalankan query dan ambil data
    df_sales_by_subcategory = run_query(query_sales_by_subcategory)

    # Visualisasi menggunakan Plotly
    st.header('COMPOSITION: Penjualan Berdasarkan Subkategori Produk')
    colors = ['#402E7A', '#4C3BCF', '#4B70F5', '#3DC2EC']
    fig = px.area(
        df_sales_by_subcategory, 
        x='CalendarYear', 
        y='TotalSales', 
        color='EnglishProductSubcategoryName',
        title='Komposisi Penjualan Berdasarkan Subkategori Produk',
        labels={'TotalSales': 'Total Penjualan', 'EnglishProductSubcategoryName': 'Subkategori Produk'},
        color_discrete_sequence=colors
    )

    fig.update_traces(mode="markers+lines", hoverinfo="all")

    # Update sumbu x agar hanya menampilkan nilai tahun yang bulat
    fig.update_xaxes(tickmode='linear', dtick=1, tick0=2001)

    st.plotly_chart(fig)

    # Deskripsi visualisasi
    st.write('#### Deskripsi:')
    st.markdown("""
        <div style="text-align: justify;">
            <p>Visualisasi yang diberikan adalah stacked area chart yang menggambarkan komposisi 
            total penjualan produk dalam setiap subkategori produknya. Pada tahun 2003, terjadi 
            penjualan tertinggi dengan subkategori mountain bike mencatatkan total penjualan sebesar 4 juta, 
            sementara penjualan terendah terjadi pada kategori accessories dengan subkategori sock yang hanya 
            mencapai total penjualan 2 ribu. Hampir semua subkategori mengalami peningkatan penjualan setiap tahunnya, 
            meskipun terdapat penurunan pada subkategori road bike pada tahun 2024. Dari data ini, dapat disimpulkan 
            bahwa tren umumnya menunjukkan pertumbuhan penjualan, namun perlu perhatian khusus terhadap subkategori yang 
            mengalami penurunan untuk strategi yang lebih baik ke depannya.
            </p>
        </div>
        """, unsafe_allow_html=True)



    # VISUALISASI RELATIONSHIP
    # Visulisasi RELATIONSHIP: Penjualan dan Promosi untuk Seluruh Subkategori Produk
    query_relationship_all = '''
    SELECT 
        psc.ProductSubcategoryKey,
        psc.EnglishProductSubcategoryName,
        p.PromotionKey,
        SUM(fs.SalesAmount) AS TotalSales
    FROM 
        FactInternetSales fs
    JOIN 
        DimPromotion p ON fs.PromotionKey = p.PromotionKey
    JOIN 
        DimProduct dp ON fs.ProductKey = dp.ProductKey
    JOIN 
        DimProductSubcategory psc ON dp.ProductSubcategoryKey = psc.ProductSubcategoryKey
    GROUP BY 
        psc.ProductSubcategoryKey, psc.EnglishProductSubcategoryName, p.PromotionKey
    '''

    df_relationship_all = run_query(query_relationship_all)
    st.header('RELATIONSHIP: Penjualan dan Promosi untuk Seluruh Subkategori Produk')

    # Visualisasi 
    fig = px.scatter(
        df_relationship_all, 
        x='PromotionKey', 
        y='TotalSales', 
        color='EnglishProductSubcategoryName',
        title='Penjualan dan Promosi untuk Seluruh Subkategori Produk',
        labels={'PromotionKey': 'Promotion Key', 'TotalSales': 'Total Penjualan'},
        hover_data={'EnglishProductSubcategoryName': True, 'PromotionKey': True, 'TotalSales': True},
        color_discrete_sequence=['#0E46A3', '#1E0342', '#9AC8CD', '#E1F7F5']
    )
    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.update_layout(showlegend=True, xaxis=dict(range=[0, 15]))
    st.plotly_chart(fig)

    # Deskripsi visualisasi
    st.write('#### Deskripsi:')
    st.markdown("""
        <div style="text-align: justify;">
            <p>Visualisasi scatter plot menunjukkan hubungan antara promosi (Promotion Key) 
            dan total penjualan untuk seluruh subkategori produk. Kunci promosi dengan 
            total penjualan tertinggi adalah promosi kunci 1, yang mencapai hampir 4 juta, 
            sementara kunci promosi dengan total penjualan terendah hanya mencatat 14 ribu. 
            Pola ini mengindikasikan adanya korelasi antara intensitas promosi dan performa 
            penjualan produk.</p>
        </div>
        """, unsafe_allow_html=True)


    # VISUALISASI DISTRIBUTION
    # Query
    query_annual_sales = '''
    SELECT 
        psc.ProductSubcategoryKey,
        psc.EnglishProductSubcategoryName,
        t.CalendarYear,
        SUM(fs.SalesAmount) AS TotalSales
    FROM 
        FactInternetSales fs
    JOIN 
        DimProduct dp ON fs.ProductKey = dp.ProductKey
    JOIN 
        DimProductSubcategory psc ON dp.ProductSubcategoryKey = psc.ProductSubcategoryKey
    JOIN 
        DimTime t ON fs.OrderDateKey = t.TimeKey
    WHERE 
        t.CalendarYear BETWEEN 2001 AND 2004
    GROUP BY 
        psc.ProductSubcategoryKey, psc.EnglishProductSubcategoryName, t.CalendarYear
    ORDER BY 
        psc.ProductSubcategoryKey, t.CalendarYear
    '''

    # Jalankan query dan ambil data
    df_annual_sales = run_query(query_annual_sales)

    # Visualisasi menggunakan plotly
    st.header('DISTRIBUTION: Penjualan Tahunan untuk Setiap Subkategori Produk')

    fig = px.line(
        df_annual_sales,
        x='CalendarYear',
        y='TotalSales',
        color='EnglishProductSubcategoryName',
        markers=True,
        title='Distribusi Penjualan Tahunan untuk Setiap Subkategori Produk (2001-2004)',
        labels={'TotalSales': 'Total Penjualan', 'EnglishProductSubcategoryName': 'Subkategori Produk'},
        color_discrete_sequence=['#0E46A3', '#1E0342', '#9AC8CD', '#E1F7F5']
    )

    fig.update_traces(mode='lines+markers')

    # Atur sumbu x menjadi kategori
    fig.update_xaxes(type='category')

    # Tambahkan informasi saat grafik diklik
    fig.update_layout(clickmode='event+select')

    # Fungsi untuk menampilkan informasi saat grafik diklik
    def display_click_data(trace, points, selector):
        for point in points.point_inds:
            st.write(f"Subkategori: {df_annual_sales.iloc[point]['EnglishProductSubcategoryName']}, Tahun: {df_annual_sales.iloc[point]['CalendarYear']}, Total Penjualan: ${df_annual_sales.iloc[point]['TotalSales']:,.2f}")

    fig.data[0].on_click(display_click_data)

    # Tampilkan plot di aplikasi Streamlit
    st.plotly_chart(fig)

    # Deskripsi visualisasi
    st.write('#### Deskripsi:')
    st.markdown("""
        <div style="text-align: justify;">
            <p>Visualisasi tersebut menggambarkan dengan jelas pola penjualan tahunan untuk masing-masing subkategori produk 
            dari tahun 2001 hingga 2004. Dari data yang diberikan, terlihat bahwa subkategori mountain bike, turing bike, 
            dan beberapa kategori aksesori menunjukkan tren peningkatan yang stabil dari tahun ke tahun. Di sisi lain, 
            subkategori road bike mengalami penurunan yang cukup signifikan antara tahun 2003 dan 2004, menyoroti fluktuasi pasar dalam periode tersebut.</p>
        </div>
        """, unsafe_allow_html=True)



