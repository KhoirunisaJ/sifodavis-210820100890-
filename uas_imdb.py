import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load File Merge IMDB CSV 
file_path = 'imdbdata_3(final).csv'
data = pd.read_csv(file_path, delimiter=';')

def show_imdb_dashboard():
    # Judul Dashboard
    st.title('DASHBOARD IMDB')
    st.header("Lowest Rated Movie")
    st.write("""
    Selamat datang di dashboard IMDB by Khoirunisa!
    Dashboard ini menampilkan beberapa visualisasi untuk menganalisis Lowest Rated Movie pada website IMDB. 
    Nikmati eksplorasi data Anda!
    """)

    # Membuat Filter Dopdown - year
    default_year = 2002
    years = sorted(data['Year'].unique())
    selected_year = st.selectbox('Pilih Tahun:', years, index=years.index(default_year) if default_year in years else len(years) - 1)

    # Memfilter Data Berdasarkan Tahun yang Dipilih
    filtered_data = data[data['Year'] == selected_year]

    # VISUALISASI
    # 1. Visualisasi komposisi berdasarkan kategori Rating (Donut Chart)
    st.write("## COMPOSITION: Film Berdasarkan Rating")
    rating_counts = filtered_data['Rating'].value_counts().reset_index()
    rating_counts.columns = ['Rating', 'Count']
    fig = px.pie(rating_counts, values='Count', names='Rating',
                title=f'Komposisi Film Berdasarkan Rating {selected_year}',
                color_discrete_sequence=px.colors.sequential.RdBu, hole=0.3)
    fig.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}')
    st.plotly_chart(fig)
    # Deskripsi
    st.write('#### Deskripsi:')
    st.markdown("""
        <div style="text-align: justify;">
            <p>Visualisasi di atas adalah pie chart untuk komposisi rating dari setiap film yang telah dirilis. 
            Komposisi rating film yang dirilis dari tahun 1983 hingga 2023 bervariasi dari waktu ke waktu. Beberapa tahun mungkin hanya memiliki satu jenis rating
            yang dominan untuk film-film yang dirilis, sementara tahun-tahun lain menunjukkan adanya variasi dengan film-film yang memiliki beberapa jenis rating.
            Hal ini menunjukkan bahwa preferensi penonton atau kebijakan sensor film mungkin telah mengalami perubahan dari tahun ke tahun. Tren ini juga dapat mencerminkan 
            evolusi dalam industri film terkait dengan pendekatan yang berbeda terhadap konten film dan sasaran audiens. 
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 3. Visualisasi DISTRIBUTION: Durasi Film 
    st.write(f"## DISTRIBUTION: Durasi Film {selected_year}")
    fig = px.histogram(filtered_data, x='Durasi(Menit)', color='Rating', nbins=20,
                    title=f'Distribusi Durasi Film {selected_year}',
                    labels={'Durasi(Menit)': 'Durasi (Menit)', 'count': 'Frekuensi'},
                    color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(hoverinfo='x+y',
                    hovertemplate='<b>Durasi (Menit): %{x}</b><br>Frekuensi: %{y}<br>Rating: %{color}',
                    selector=dict(type='bar'))
    fig.update_layout(yaxis=dict(range=[0, 5]))
    st.plotly_chart(fig)

    # Deskripsi
    st.write('#### Deskripsi:')
    st.markdown("""
        <div style="text-align: justify;">
            <p> Visualisasi histogram ini memberikan gambaran tentang bagaimana durasi film bervariasi dari tahun ke tahun, 
            tergantung pada tahun yang dipilih dari filter dropdown di atas. Analisis menunjukkan bahwa durasi film tidak selalu 
            dipengaruhi secara langsung oleh rating film. Meskipun ada kecenderungan bahwa beberapa jenis film, 
            seperti film-film dengan rating PG-13 atau R, cenderung memiliki durasi yang lebih panjang untuk mengeksplorasi 
            plot yang kompleks atau tema yang lebih dalam, ada juga banyak variabilitas dalam durasi film di setiap rating.
            </p>
        </div>
        """, unsafe_allow_html=True)


    # 3. Visualisasi Relationship antara Rating dan Gross_World / ALL FILM (scatter plot)
    st.write("## RELATIONSHIP: antara Rating dan Gross World (All Film)")
    fig = px.scatter(data, x='Rating', y='Gross_World', size='Gross_World',
                    title='Relationship antara Rating dan Gross World',
                    labels={'Rating': 'Rating', 'Gross_World': 'Gross World', 'size': 'Gross World'},
                    color_discrete_sequence=px.colors.sequential.RdBu,
                    hover_name='Name',
                    hover_data={'Rating': True, 'Gross_World': True})
    st.plotly_chart(fig)
    # Deskripsi
    st.write('#### Deskripsi:')
    st.markdown("""
        <div style="text-align: justify;">
            <p>Visualisasi di atas adalah scatter plot yang menggambarkan relasi antara rating dan
            gross world. Terdapat hubungan antara rating film (seperti PG-13, PG, dan not rated) dengan total gross world (total pendapatan kotor global). 
            Film dengan rating PG-13, khususnya film "Batman & Robin", menunjukkan total pendapatan kotor tertinggi. Sementara itu, film-film dengan rating 
            not rated memiliki total pendapatan kotor terendah.
            Hal ini menunjukkan bahwa rating film dapat mempengaruhi potensi keuntungan yang dapat diperoleh dari film tersebut. Film dengan rating yang lebih tinggi 
            seperti PG-13 dan PG mungkin memiliki daya tarik yang lebih besar terhadap penonton, yang dapat berkontribusi pada pendapatan kotor yang lebih tinggi. 
            Sebaliknya, film-film dengan rating not rated mungkin menghadapi tantangan dalam menarik penonton atau mendapatkan distribusi yang luas, yang berdampak
            pada pendapatan kotor yang lebih rendah.  </p>
        </div>
        """, unsafe_allow_html=True)

    # 4. Visualisasi Komparasi Total Budget dan Gross US per Tahun (bar chart)
    grouped_data = data.groupby('Year').sum().reset_index()
    st.write("## COMPARISON: Total Budget dan Gross US per Tahun")
    selected_years = st.multiselect('Pilih Tahun untuk Komparasi:', grouped_data['Year'].unique(), default=grouped_data['Year'].unique())
    filtered_data = grouped_data[grouped_data['Year'].isin(selected_years)]
    fig = px.bar(filtered_data, x='Year', y=['Budget', 'Gross_US'],
                title='Komparasi Total Budget dan Gross US per Tahun',
                labels={'Year': 'Tahun Rilis', 'value': 'Total', 'variable': 'Jenis'},
                color_discrete_sequence=['#C24641', '#800000'],
                barmode='group')
    fig.update_traces(hovertemplate='<b>Tahun:</b> %{x}<br><b>Total:</b> %{y}', selector=dict(type='bar'))
    st.plotly_chart(fig)
    # Deskripsi
    st.write('#### Deskripsi:')
    st.markdown("""
        <div style="text-align: justify;">
            <p>Visualisasi tersebut menggambarkan perbandingan antara total anggaran (budget) dan pendapatan kotor (gross) 
            film-film yang dirilis di Amerika Serikat dari tahun 1983 hingga 2023. Dari data yang terlihat, rata-rata total 
            anggaran film lebih tinggi daripada pendapatan kotor mereka. Hal ini menunjukkan bahwa rendahnya rating film juga 
            berpotensi mempengaruhi laba atau keuntungan produksi film.  </p>
        </div>
        """, unsafe_allow_html=True)
