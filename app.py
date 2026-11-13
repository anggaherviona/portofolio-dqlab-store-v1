"""
Portofolio Data Analyst - Angga Herviona Ikhwanudin
Seluruh grafik dan query berasal dari latihan DQLab yang dikerjakan penulis
(Data Visualization with Python Matplotlib Part 1 & 2, Project Data Analysis for Retail).
Jalankan lokal:  streamlit run app.py
"""
from pathlib import Path
import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Kinerja Penjualan DQLab Store 2019", page_icon="📊", layout="wide")


def tampilkan():
    """Menampilkan grafik Matplotlib yang sedang aktif ke Streamlit."""
    st.pyplot(plt.gcf())
    plt.close("all")


@st.cache_data
def muat_data():
    dataset = pd.read_csv(Path(__file__).parent / "data" / "retail_raw_reduced.csv")
    dataset['order_month'] = dataset['order_date'].apply(
        lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").strftime('%Y-%m'))
    dataset['gmv'] = dataset['item_price'] * dataset['quantity']
    return dataset


dataset = muat_data()
dataset_dki_q4 = dataset[(dataset['province'] == 'DKI Jakarta') & (dataset['order_month'] >= '2019-10')]
top_brands = (dataset[dataset['order_month'] == '2019-12'].groupby('brand')['quantity']
              .sum()
              .reset_index()
              .sort_values(by='quantity', ascending=False)
              .head(5))
dataset_top5brand_dec = dataset[(dataset['order_month'] == '2019-12') &
                                (dataset['brand'].isin(top_brands['brand'].to_list()))]

# ------------------------------------------------------------------ SIDEBAR
with st.sidebar:
    st.info(
        "**Dataset**\n\n"
        "Data yang digunakan dalam artikel ini bersumber dari dataset pelatihan DQLab:\n\n"
        "1. [retail_raw_reduced.csv](https://dqlabcdn.xeratic.com/dqlab-dataset/retail_raw_reduced.csv) "
        "(transaksi Juli-Desember 2019)\n"
        "2. Tabel `dqlab_sales_store` (penjualan 2009-2012, dianalisis dengan SQL)"
    )
    st.info(
        "**Catatan**\n\n"
        "GMV (Gross Merchandise Value) dihitung sebagai `item_price × quantity`.\n\n"
        "Seluruh grafik dan query di halaman ini dikerjakan penulis selama pelatihan DQLab: "
        "*Data Visualization with Python Matplotlib for Beginner Part 1 & 2* dan "
        "*Project Data Analysis for Retail: Sales Performance Report*."
    )
    st.success(
        "**Angga Herviona Ikhwanudin**\n\n"
        "Pranata Laboratorium Pendidikan di Laboratorium Teknologi Rekayasa Pangan, "
        "Politeknik Negeri Jember. Sedang belajar analisis data dengan Python dan SQL di DQLab."
    )

# ------------------------------------------------------------------ PEMBUKA
st.title("Kinerja Penjualan DQLab Store: Siapa, Di Mana, dan Apa yang Dibeli?")
st.markdown("Penulis : **Angga Herviona Ikhwanudin**")
st.write(
    "DQLab Store adalah toko retail online yang melayani pelanggan di tujuh provinsi di Jawa dan Bali. Sepanjang Juli-Desember 2019, toko ini mencatat 5.000 baris transaksi dengan total GMV sekitar Rp33 miliar."
)
st.write(
    "Artikel ini mencoba menjawab tiga pertanyaan: kapan penjualan meningkat, di mana dan oleh siapa penjualan terjadi, serta produk apa yang paling laku. Data 2019 dianalisis dengan Python (pandas dan Matplotlib), sedangkan data penjualan 2009-2012 dianalisis dengan SQL."
)
st.write(
    "Pembahasan disusun berurutan. Bagian 1 melihat tren GMV secara keseluruhan. Bagian 2 menelusuri DKI Jakarta sebagai penyumbang terbesar. Bagian 3 mempelajari perilaku customer. Bagian 4 membahas brand terlaris di bulan puncak. Bagian 5 mengevaluasi efektivitas promosi dengan SQL."
)

# ------------------------------------------------------------------ BAGIAN 1
st.header("1. Tren GMV Bulanan 2019")
st.write(
    "Langkah pertama adalah melihat gambaran besar: bagaimana GMV bergerak dari bulan ke bulan, lalu brand dan provinsi mana yang mendorong pergerakan tersebut."
)

st.subheader("Gambar 1. Monthly GMV Year 2019")
fig = plt.figure(figsize=(15, 5))
dataset.groupby(['order_month'])['gmv'].sum().plot(color='green', marker='o', linestyle='-.', linewidth=2)
plt.title('Monthly GMV Year 2019', loc='center', pad=20, fontsize=20, color='blue')
plt.xlabel('Order Month', fontsize=15)
plt.ylabel('Total Amount (in Billions)', fontsize=15)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000000).astype(int))
plt.text(0.45, 0.72, 'The GMV increased significantly on October 2019', transform=fig.transFigure, color='red')
tampilkan()
st.write(
    "Gambar 1 menunjukkan GMV relatif stabil di kuartal ketiga, yaitu sekitar Rp3,5 miliar (Juli), Rp4,5 miliar (Agustus), dan Rp3,9 miliar (September). Pada Oktober, GMV melonjak menjadi sekitar Rp6,7 miliar, naik sekitar 70% hanya dalam satu bulan."
)
st.write(
    "Setelah sedikit turun di November (sekitar Rp6,2 miliar), GMV mencapai titik tertinggi di Desember, sekitar Rp8,1 miliar atau 2,3 kali GMV Juli. Lonjakan ini memunculkan pertanyaan berikutnya: siapa yang mendorong kenaikan tersebut?"
)

st.subheader("Gambar 2. Monthly GMV Year 2019 - Breakdown by Brand")
dataset.groupby(['order_month', 'brand'])['gmv'].sum().unstack().plot()
plt.title('Monthly GMV Year 2019 - Breakdown by Brand', loc='center', pad=30, fontsize=20, color='blue')
plt.xlabel('Order Month', fontsize=15)
plt.ylabel('Total Amount (in Billions)', fontsize=15)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000000).astype(int))
plt.legend(loc='right', bbox_to_anchor=(1.6, 0.5), shadow=True, ncol=2)
plt.gcf().set_size_inches(12, 5)
plt.tight_layout()
tampilkan()
st.write(
    "Gambar 2 memecah GMV menurut brand. Kenaikan di kuartal keempat ternyata terjadi merata: kesepuluh brand mencatat GMV Oktober-Desember yang lebih tinggi dibanding Juli-September."
)
st.write(
    "BRAND_S memimpin GMV di kuartal ketiga. Namun, pada Oktober dan Desember, posisi teratas diambil alih BRAND_R, yang GMV-nya melonjak dari sekitar Rp0,45 miliar di September menjadi sekitar Rp1,2 miliar di Oktober."
)
st.write(
    "Karena kenaikan terjadi di semua brand, lonjakan GMV kemungkinan besar dipicu oleh faktor umum seperti musim belanja akhir tahun, bukan oleh satu brand saja."
)

st.subheader("Gambar 3. Monthly GMV Year 2019 - Breakdown by Province")
dataset.groupby(['order_month', 'province'])['gmv'].sum().unstack().plot(cmap='Set1', figsize=(10, 6))
plt.title('Monthly GMV Year 2019 - Breakdown by Province', loc='center', pad=30, fontsize=20, color='blue')
plt.xlabel('Order Month', fontsize=15)
plt.ylabel('Total Amount (in Billions)', fontsize=15)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000000).astype(int))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=4, title='Province',
           fontsize=9, title_fontsize=11)
plt.subplots_adjust(bottom=0.3)
tampilkan()
st.write(
    "Dari sisi wilayah, Gambar 3 memperlihatkan satu provinsi yang berada jauh di atas provinsi lain: DKI Jakarta. Garis DKI Jakarta selalu berada di posisi teratas dan menyumbang hampir separuh GMV. Jawa Barat berada di urutan kedua, sementara Banten dan Bali memiliki GMV paling kecil."
)
st.write(
    "Garis DKI Jakarta juga mengikuti pola Gambar 1: turun di September, lalu melonjak tajam di Oktober. Namun, dengan tujuh garis berwarna, grafik ini cukup ramai dibaca. Karena itu, Gambar 4 menyederhanakannya."
)

st.subheader("Gambar 4. Monthly GMV Year 2019 - Top 5 Provinsi dan Lainnya")
top_provinces = (dataset.groupby('province')['gmv']
                 .sum()
                 .reset_index()
                 .sort_values(by='gmv', ascending=False)
                 .head(5))
dataset['province_top'] = dataset['province'].apply(
    lambda x: x if (x in top_provinces['province'].to_list()) else 'other')
dataset.groupby(['order_month', 'province_top'])['gmv'].sum().unstack().plot(marker='.', cmap='plasma')
plt.title('Monthly GMV Year 2019 - Breakdown by Province', loc='center', pad=30, fontsize=20, color='blue')
plt.xlabel('Order Month', fontsize=15)
plt.ylabel('Total Amount (in Billions)', fontsize=15)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000000).astype(int))
plt.legend(loc='upper center', bbox_to_anchor=(1.1, 1), shadow=True, ncol=1)
plt.annotate('GMV other meningkat pesat', xy=(5, 900000000),
             xytext=(4, 1700000000), weight='bold', color='red',
             arrowprops=dict(arrowstyle='fancy', connectionstyle='arc3', color='red'))
plt.annotate('DKI Jakarta mendominasi', xy=(3, 3350000000),
             xytext=(0, 3700000000), weight='bold', color='red',
             arrowprops=dict(arrowstyle='->', connectionstyle='angle', color='red'))
plt.gcf().set_size_inches(12, 5)
plt.tight_layout()
tampilkan()
st.write(
    "Gambar 4 hanya menampilkan lima provinsi dengan GMV terbesar, sedangkan dua provinsi lainnya (Banten dan Bali) digabung menjadi kategori other. Dua hal menonjol dan diberi anotasi."
)
st.write(
    "Pertama, DKI Jakarta mendominasi di setiap bulan, dengan puncak GMV sekitar Rp3,5 miliar di Desember. Kedua, kategori other melonjak di Desember, hampir tiga kali lipat dibanding November. Jawa Tengah juga naik tajam di bulan yang sama."
)
st.write(
    "Artinya, di bulan puncak, pertumbuhan tidak hanya datang dari Jakarta. Provinsi-provinsi yang lebih kecil juga ikut menyumbang kenaikan."
)

st.subheader("Gambar 5. Daily Number of Customers - December 2019")
plt.figure(figsize=(10, 5))
dataset[dataset['order_month'] == '2019-12'].groupby(['order_date'])['customer_id'].nunique().plot(
    color='red', marker='.', linewidth=2)
plt.title('Daily Number of Customers - December 2019', loc='left', pad=20, fontsize=20, color='orange')
plt.xlabel('Order Date', fontsize=15, color='blue')
plt.ylabel('Number of Customers', fontsize=15, color='blue')
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
tampilkan()
st.write(
    "Gambar 5 memperbesar bulan puncak, Desember 2019, hingga ke tingkat harian. Rata-rata sekitar 31 customer bertransaksi setiap hari, dengan jumlah tertinggi 40 customer pada 1 Desember dan terendah 19 customer pada 27 Desember."
)
st.write(
    "Jumlah customer harian naik turun tanpa tren yang jelas. Dengan demikian, tingginya GMV Desember tidak berasal dari satu atau dua hari tertentu, melainkan dari aktivitas belanja yang ramai sepanjang bulan. Beberapa penurunan terdalam terjadi menjelang akhir tahun (27 dan 29 Desember), kemungkinan bertepatan dengan masa libur."
)

# ------------------------------------------------------------------ BAGIAN 2
st.header("2. Fokus DKI Jakarta, Kuartal 4 2019")
st.write(
    "Karena DKI Jakarta menyumbang hampir separuh GMV, bagian ini menelusuri penjualan di DKI Jakarta lebih dalam, khususnya pada kuartal keempat 2019 (Oktober-Desember), periode dengan GMV tertinggi."
)

st.subheader("Gambar 6. GMV Contribution Per City - DKI Jakarta in Q4 2019")
gmv_per_city_dki_q4 = dataset_dki_q4.groupby('city')['gmv'].sum().reset_index()
plt.figure(figsize=(6, 6))
plt.pie(gmv_per_city_dki_q4['gmv'], labels=gmv_per_city_dki_q4['city'], autopct='%1.2f%%')
plt.title('GMV Contribution Per City - DKI Jakarta in Q4 2019', loc='center', pad=30, fontsize=15, color='blue')
kol1, kol2 = st.columns([1, 1])
with kol1:
    tampilkan()
with kol2:
    st.write(
        "Jakarta Selatan menyumbang porsi terbesar, yaitu 36,23% GMV DKI Jakarta di Q4 2019, "
        "diikuti Jakarta Pusat (24,99%). Kedua kota ini bersama-sama menyumbang lebih dari 61% GMV."
    )
    st.write(
        "Tiga kota lainnya, Jakarta Barat (14,58%), Jakarta Timur (12,29%), dan Jakarta Utara (11,92%), "
        "memiliki porsi yang relatif mirip."
    )

st.subheader("Gambar 7. GMV Per City - DKI Jakarta in Q4 2019")
plt.clf()
dataset_dki_q4.groupby('city')['gmv'].sum().sort_values(ascending=False).plot(kind='bar', color='green')
plt.title('GMV Per City - DKI Jakarta in Q4 2019', loc='center', pad=30, fontsize=15, color='blue')
plt.xlabel('City', fontsize=15)
plt.ylabel('Total Amount (in Billions)', fontsize=15)
plt.ylim(ymin=0)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000000).astype(int))
plt.xticks(rotation=0)
tampilkan()
st.write(
    "Gambar 7 menyajikan data yang sama dalam bentuk diagram batang yang sudah diurutkan, sehingga selisih antarkota lebih mudah dibandingkan. GMV Jakarta Selatan sekitar Rp3,4 miliar, kira-kira tiga kali GMV Jakarta Utara (sekitar Rp1,1 miliar). Lalu, apakah pola ini sama di setiap bulan?"
)

st.subheader("Gambar 8. GMV Per City, Breakdown by Month")
dataset_dki_q4.groupby(['city', 'order_month'])['gmv'].sum().unstack().plot(kind='bar')
plt.title('GMV Per City, Breakdown by Month\nDKI Jakarta in Q4 2019', loc='center', pad=30, fontsize=15,
          color='blue')
plt.xlabel('Province', fontsize=12)
plt.ylabel('Total Amount (in Billions)', fontsize=12)
plt.legend(bbox_to_anchor=(1, 1), shadow=True, title='Month')
plt.ylim(ymin=0)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000000).astype(int))
plt.xticks(rotation=45)
plt.tight_layout()
tampilkan()
st.write(
    "Gambar 8 menunjukkan bahwa jawabannya tidak. Jakarta Selatan mencapai puncak di Oktober (sekitar Rp1,5 miliar), lalu turun di November dan Desember (sekitar Rp1,0 miliar). Jakarta Pusat juga cenderung menurun dari bulan ke bulan."
)
st.write(
    "Sebaliknya, Jakarta Barat naik setiap bulan, dan Jakarta Utara melonjak di Desember hingga lebih dari dua kali lipat GMV November. Jakarta Timur juga naik di Desember setelah sempat turun di November."
)

st.subheader("Gambar 9. GMV Per Month, Breakdown by City")
dataset_dki_q4.groupby(['order_month', 'city'])['gmv'].sum().sort_values(ascending=False).unstack().plot(
    kind='bar', stacked=True)
plt.title('GMV Per Month, Breakdown by City\nDKI Jakarta in Q4 2019', loc='center', pad=30, fontsize=15,
          color='blue')
plt.xlabel('Order Month', fontsize=12)
plt.ylabel('Total Amount (in Billions)', fontsize=12)
plt.legend(bbox_to_anchor=(1, 1), shadow=True, ncol=1, title='City')
plt.ylim(ymin=0)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000000).astype(int))
plt.xticks(rotation=0)
plt.tight_layout()
tampilkan()
st.write(
    "Gambar 9 menyajikan sudut pandang sebaliknya: total GMV DKI Jakarta per bulan beserta komposisi kotanya. Pada Oktober, total GMV paling banyak disumbang Jakarta Selatan. Pada Desember, porsi Jakarta Selatan mengecil, tetapi total GMV justru naik karena kenaikan di Jakarta Barat, Timur, dan Utara."
)
st.write(
    "Ini menunjukkan bahwa penjualan di DKI Jakarta mulai lebih merata di akhir tahun dan tidak lagi hanya bertumpu pada Jakarta Selatan."
)

# ------------------------------------------------------------------ BAGIAN 3
st.header("3. Perilaku Customer DKI Jakarta Q4 2019")
st.write(
    "Setelah mengetahui di mana penjualan terjadi, pertanyaan berikutnya adalah siapa yang berbelanja. Bagian ini menganalisis customer DKI Jakarta di Q4 2019 berdasarkan tiga ukuran per customer: jumlah order, jumlah barang (quantity), dan total belanja (GMV)."
)
data_per_customer = (dataset_dki_q4.groupby('customer_id')
                     .agg({'order_id': 'nunique',
                           'quantity': 'sum',
                           'gmv': 'sum'})
                     .reset_index()
                     .rename(columns={'order_id': 'orders'}))

st.subheader("Gambar 10. Distribution of Number of Orders per Customer")
plt.figure()
plt.hist(data_per_customer['orders'], range=(1, 5))
plt.title('Distribution of Number of Orders per Customer\nDKI Jakarta in Q4 2019', fontsize=15, color='blue')
plt.xlabel('Number of Orders', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
kol1, kol2 = st.columns([1, 1])
with kol1:
    tampilkan()
with kol2:
    st.write(
        "Gambar 10 menunjukkan bahwa sebagian besar customer hanya berbelanja satu kali, yaitu sekitar "
        "500 orang. Sekitar 150 customer berbelanja dua kali, sekitar 40 customer tiga kali, dan "
        "hanya segelintir yang berbelanja empat kali atau lebih."
    )
    st.write(
        "Pola ini menandakan loyalitas customer masih rendah: banyak orang mencoba berbelanja, "
        "tetapi sedikit yang kembali dalam periode yang sama."
    )

st.subheader("Gambar 11. Distribution of Total Quantity per Customer")
plt.figure(figsize=(10, 5))
plt.hist(data_per_customer['quantity'], bins=100, range=(1, 200), color='brown')
plt.title('Distribution of Total Quantity per Customer\nDKI Jakarta in Q4 2019', fontsize=15, color='blue')
plt.xlabel('Quantity', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.xlim(xmin=0, xmax=200)
tampilkan()
st.write(
    "Dari sisi jumlah barang, Gambar 11 memperlihatkan distribusi yang sangat miring ke kanan. Batang-batang tertinggi berada di bawah 25 unit, artinya sebagian besar customer membeli dalam jumlah kecil selama Q4 2019. Hanya sedikit customer yang membeli lebih dari 100 unit, yang kemungkinan merupakan pembelian grosir."
)

st.subheader("Gambar 12. Distribution of Total GMV per Customer")
plt.figure(figsize=(10, 5))
plt.hist(data_per_customer['gmv'], bins=100, range=(1, 200000000), color='green')
plt.title('Distribution of Total GMV per Customer\nDKI Jakarta in Q4 2019', fontsize=15, color='blue')
plt.xlabel('GMV (in Millions)', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.xlim(xmin=0, xmax=200000000)
labels, locations = plt.xticks()
plt.xticks(labels, (labels/1000000).astype(int))
tampilkan()
st.write(
    "Pola serupa terlihat pada total belanja (Gambar 12). Sebagian besar customer berbelanja kurang dari Rp25 juta selama Q4 2019, dengan kelompok terbanyak di kisaran Rp2-10 juta. Di ujung kanan, ada sebagian kecil customer yang berbelanja sangat besar, bahkan lebih dari Rp100 juta."
)

st.subheader("Gambar 13. Correlation of Quantity and GMV per Customer")
plt.figure(figsize=(10, 8))
plt.scatter(data_per_customer['quantity'], data_per_customer['gmv'], marker='+', color='red')
plt.title('Correlation of Quantity and GMV per Customer\nDKI Jakarta in Q4 2019', fontsize=15, color='blue')
plt.xlabel('Quantity', fontsize=12)
plt.ylabel('GMV (in Millions)', fontsize=12)
plt.xlim(xmin=0, xmax=300)
plt.ylim(ymin=0, ymax=150000000)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000).astype(int))
tampilkan()
st.write(
    "Gambar 13 menghubungkan kedua ukuran tersebut. Titik-titik membentuk pola naik dari kiri bawah ke kanan atas: customer yang membeli lebih banyak barang cenderung menghasilkan GMV yang lebih besar. Artinya, quantity dan GMV per customer berkorelasi positif."
)
st.write(
    "Meski begitu, sebaran titik melebar pada quantity besar. Dua customer dengan jumlah barang yang sama bisa menghasilkan GMV yang sangat berbeda, karena GMV juga bergantung pada harga barang yang dibeli."
)

# ------------------------------------------------------------------ BAGIAN 4
st.header("4. Top 5 Brand Desember 2019")
st.write(
    "Bagian ini kembali ke bulan dengan GMV tertinggi, Desember 2019, dan berfokus pada lima brand dengan quantity terjual terbanyak. Data difilter menjadi transaksi Desember 2019 untuk kelima brand tersebut, lalu dianalisis dari sisi penjualan harian, jumlah produk, dan harga."
)

st.subheader("Tabel 1. Top 5 Brand Berdasarkan Quantity, Desember 2019")
st.dataframe(top_brands, hide_index=True)
st.write(
    "BRAND_S (2.197 unit) dan BRAND_P (2.194 unit) hampir seimbang di posisi teratas, disusul BRAND_R (1.508 unit), BRAND_C (1.365 unit), dan BRAND_A (1.315 unit)."
)

st.subheader("Gambar 14. Daily Sold Quantity Dec 2019 - Breakdown by Brands")
dataset_top5brand_dec.groupby(['order_date', 'brand'])['quantity'].sum().unstack().plot(marker='.', cmap='plasma')
plt.title('Daily Sold Quantity Dec 2019 - Breakdown by Brands', loc='center', pad=30, fontsize=15, color='blue')
plt.xlabel('Order Date', fontsize=12)
plt.ylabel('Quantity', fontsize=12)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
plt.legend(loc='upper center', bbox_to_anchor=(1.1, 1), shadow=True, ncol=1)
plt.annotate('Terjadi lonjakan', xy=(7, 310), xytext=(8, 300),
             weight='bold', color='red',
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3", color='red'))
plt.gcf().set_size_inches(10, 5)
plt.tight_layout()
tampilkan()
st.write(
    "Gambar 14 memperlihatkan quantity terjual harian kelima brand. Penjualan harian setiap brand naik turun cukup tajam, dengan beberapa puncak di hari-hari tertentu."
)
st.write(
    "Lonjakan tertinggi dialami BRAND_P pada 9 Desember 2019, yaitu 312 unit dalam sehari, jauh di atas hari-hari lainnya. Lonjakan lain terlihat pada BRAND_S (10 Desember, 254 unit) dan BRAND_R (18 Desember, 246 unit). Lonjakan seperti ini kemungkinan terkait promo atau pembelian dalam jumlah besar oleh customer tertentu."
)

st.subheader("Gambar 15. Number of Sold Products per Brand, December 2019")
plt.clf()
dataset_top5brand_dec.groupby('brand')['product_id'].nunique().sort_values(ascending=False).plot(
    kind='bar', color='green')
plt.title('Number of Sold Products per Brand, December 2019', loc='center', pad=30, fontsize=15, color='blue')
plt.xlabel('Brand', fontsize=15)
plt.ylabel('Number of Products', fontsize=15)
plt.ylim(ymin=0)
plt.xticks(rotation=0)
tampilkan()
st.write(
    "Gambar 15 menghitung jumlah produk berbeda yang terjual dari setiap brand. BRAND_S unggul jauh dengan sekitar 150 produk, diikuti BRAND_P (sekitar 100 produk), BRAND_R dan BRAND_C (masing-masing sekitar 85 produk), lalu BRAND_A (sekitar 70 produk)."
)
st.write(
    "Urutan ini sama persis dengan urutan quantity di Tabel 1. Brand dengan variasi produk lebih banyak cenderung menjual lebih banyak unit."
)

st.subheader("Gambar 16. Produk Terjual >= 100 dan < 100 Unit per Brand")
dataset_top5brand_dec_per_product = dataset_top5brand_dec.groupby(['brand', 'product_id'])['quantity'].sum().reset_index()
dataset_top5brand_dec_per_product['quantity_group'] = dataset_top5brand_dec_per_product['quantity'].apply(
    lambda x: '>= 100' if x >= 100 else '< 100')
dataset_top5brand_dec_per_product.sort_values('quantity', ascending=False, inplace=True)
s_sort = dataset_top5brand_dec_per_product.groupby('brand')['product_id'].nunique().sort_values(ascending=False)
dataset_top5brand_dec_per_product.groupby(['brand', 'quantity_group'])['product_id'].nunique().reindex(
    index=s_sort.index, level='brand').unstack().plot(kind='bar', stacked=True)
plt.title('Number of Sold Products per Brand, December 2019', loc='center', pad=30, fontsize=15, color='blue')
plt.xlabel('Brand', fontsize=15)
plt.ylabel('Number of Products', fontsize=15)
plt.ylim(ymin=0)
plt.xticks(rotation=0)
tampilkan()
st.write(
    "Gambar 16 memecah batang pada Gambar 15 menjadi produk yang terjual 100 unit atau lebih dan produk yang terjual kurang dari 100 unit. Hampir semua produk masuk kelompok kurang dari 100 unit. Produk yang terjual 100 unit atau lebih hanya segelintir di setiap brand, dan BRAND_C tidak memiliki satu pun."
)
st.write(
    "Artinya, tingginya quantity brand-brand ini tidak bertumpu pada satu atau dua produk andalan, melainkan pada banyak produk yang masing-masing terjual dalam jumlah sedang. Temuan ini menguatkan Gambar 15: luasnya variasi produk adalah kunci."
)

st.subheader("Gambar 17. Distribution of Price Median per Product")
plt.figure(figsize=(10, 5))
plt.hist(dataset_top5brand_dec.groupby('product_id')['item_price'].median(), bins=10, stacked=True,
         range=(1, 2000000), color='green')
plt.title('Distribution of Price Median per Product\nTop 5 Brands in Dec 2019', fontsize=15, color='blue')
plt.xlabel('Price Median', fontsize=12)
plt.ylabel('Number of Products', fontsize=12)
plt.xlim(xmin=0, xmax=2000000)
tampilkan()
st.write(
    "Gambar 17 melihat sisi harga. Untuk setiap produk diambil median harganya, lalu sebarannya digambarkan dalam histogram. Kelompok terbesar berada pada rentang Rp400-600 ribu, yaitu sekitar 125 produk."
)
st.write(
    "Sebagian besar produk berharga di bawah Rp800 ribu, dan jumlahnya makin sedikit pada harga yang lebih tinggi. Sebagai catatan, histogram ini dibatasi sampai Rp2 juta, sehingga 43 produk yang harganya di atas Rp2 juta tidak ikut tergambar. Dengan kata lain, produk top 5 brand didominasi kelas harga murah hingga menengah."
)

data_per_product_top5brand_dec = dataset_top5brand_dec.groupby('product_id').agg(
    {'quantity': 'sum', 'gmv': 'sum', 'item_price': 'median'}).reset_index()

st.subheader("Gambar 18. Correlation of Quantity and GMV per Product")
plt.figure(figsize=(10, 8))
plt.scatter(data_per_product_top5brand_dec['quantity'], data_per_product_top5brand_dec['gmv'],
            marker='+', color='red')
plt.title('Correlation of Quantity and GMV per Product\nTop 5 Brands in December 2019', fontsize=15,
          color='blue')
plt.xlabel('Quantity', fontsize=12)
plt.ylabel('GMV (in Millions)', fontsize=12)
plt.xlim(xmin=0, xmax=300)
plt.ylim(ymin=0, ymax=200000000)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000).astype(int))
tampilkan()
st.write(
    "Gambar 18 dan Gambar 19 menjawab dua pertanyaan lanjutan: apakah produk yang laku banyak menghasilkan GMV besar, dan apakah produk murah lebih banyak dibeli?"
)
st.write(
    "Pada Gambar 18, quantity dan GMV per produk berkorelasi positif: makin banyak unit terjual, makin besar GMV-nya. Namun, sebarannya lebar. Ada produk yang terjual sekitar 230 unit dengan GMV hanya sekitar Rp44 juta, sementara produk lain yang terjual sekitar 75 unit sudah menghasilkan GMV lebih dari Rp130 juta. Perbedaan ini disebabkan oleh harga produk."
)

st.subheader("Gambar 19. Price Median vs Quantity per Product")
plt.figure(figsize=(10, 8))
plt.scatter(data_per_product_top5brand_dec['item_price'], data_per_product_top5brand_dec['quantity'],
            marker='o', color='green')
plt.title('Correlation of Quantity and GMV per Product\nTop 5 Brands in December 2019', fontsize=15,
          color='blue')
plt.xlabel('Price Median', fontsize=12)
plt.ylabel('Quantity', fontsize=12)
plt.xlim(xmin=0, xmax=2000000)
plt.ylim(ymin=0, ymax=250)
tampilkan()
st.write(
    "Gambar 19 menjawab pertanyaan kedua. Titik-titiknya menyebar tanpa pola naik atau turun yang jelas: produk murah maupun mahal sebagian besar terjual kurang dari 50 unit. Beberapa produk dengan quantity sangat tinggi (lebih dari 150 unit) memang berharga di bawah Rp1,1 juta, tetapi produk murah tidak otomatis dibeli lebih banyak."
)
st.write(
    "Titik-titik yang membentuk garis vertikal menunjukkan banyak produk dengan median harga yang sama persis. Kesimpulannya, harga bukan faktor utama yang menentukan jumlah pembelian di top 5 brand."
)

# ------------------------------------------------------------------ BAGIAN 5
st.header("5. Kinerja Penjualan dan Promosi 2009-2012 (SQL)")
st.write(
    "Bagian terakhir beralih ke data penjualan jangka panjang (2009-2012) pada tabel dqlab_sales_store, yang dianalisis dengan SQL. Hanya order berstatus 'Order Finished' yang dihitung, agar order yang batal tidak ikut menambah angka penjualan. Query dan hasilnya ditampilkan di setiap tabel."
)

st.subheader("Tabel 2. Overall Performance by Year")
st.code("""SELECT
  YEAR(order_date) AS years,
  SUM(sales) AS sales,
  COUNT(order_status) AS number_of_order
FROM dqlab_sales_store
WHERE order_status = 'Order Finished'
GROUP BY YEAR(order_date)
ORDER BY YEAR(order_date);""", language="sql")
st.dataframe(pd.DataFrame({
    "years": [2009, 2010, 2011, 2012],
    "sales": [4613872681, 4059100607, 4112036186, 4482983158],
    "number_of_order": [1244, 1248, 1178, 1254],
}), hide_index=True)
st.write(
    "Penjualan tertinggi terjadi pada 2009 (sekitar Rp4,61 miliar), turun di 2010 (sekitar Rp4,06 miliar), lalu perlahan pulih hingga sekitar Rp4,48 miliar di 2012. Jumlah order relatif stabil di kisaran 1.178-1.254 order per tahun, sehingga naik turunnya penjualan lebih banyak dipengaruhi nilai per order daripada jumlah order."
)

st.subheader("Tabel 3. Promotion Effectiveness and Efficiency by Years")
st.code("""SELECT
  years,
  sales,
  promotion_value,
  ROUND((promotion_value / sales) * 100, 2) AS burn_rate_percentage
FROM (
  SELECT
    YEAR(order_date) AS years,
    SUM(sales) AS sales,
    SUM(discount_value) AS promotion_value
  FROM dqlab_sales_store
  WHERE order_status = 'Order Finished'
  GROUP BY YEAR(order_date)
) AS a
ORDER BY years;""", language="sql")
st.dataframe(pd.DataFrame({
    "years": [2009, 2010, 2011, 2012],
    "sales": [4613872681, 4059100607, 4112036186, 4482983158],
    "promotion_value": [214330327, 197506939, 214611556, 225867642],
    "burn_rate_percentage": [4.65, 4.87, 5.22, 5.04],
}), hide_index=True)
st.write(
    "DQLab Store menetapkan burn rate promosi maksimal 4,5%. Burn rate dihitung dari total diskon dibagi total penjualan, dikali 100. Hasilnya, burn rate selalu melebihi target di keempat tahun: 4,65% (2009), 4,87% (2010), 5,22% (2011), dan 5,04% (2012)."
)
st.write(
    "Burn rate tertinggi terjadi pada 2011, ketika nilai diskon naik sementara penjualan hampir tidak berubah. Dengan demikian, promosi DQLab Store selama 2009-2012 dapat dikatakan belum efisien."
)

st.subheader("Tabel 4. Customers Transactions per Year")
st.code("""SELECT
  YEAR(order_date) AS years,
  COUNT(DISTINCT customer) AS number_of_customer
FROM dqlab_sales_store
WHERE order_status = 'Order Finished'
GROUP BY YEAR(order_date)
ORDER BY years;""", language="sql")
st.dataframe(pd.DataFrame({
    "years": [2009, 2010, 2011, 2012],
    "number_of_customer": [585, 593, 581, 594],
}), hide_index=True)
st.write(
    "Jumlah customer yang bertransaksi relatif stabil, antara 581 dan 594 customer per tahun. Jika dikaitkan dengan Tabel 3, nilai diskon yang terus besar ternyata belum berhasil menambah jumlah customer secara berarti."
)

# ------------------------------------------------------------------ PENUTUP
st.header("Kesimpulan")
st.markdown("""
1. **GMV melonjak di akhir tahun.** GMV naik tajam mulai Oktober 2019 dan memuncak di Desember. Kenaikan terjadi di semua brand, sehingga kemungkinan besar dipicu musim belanja akhir tahun.
2. **DKI Jakarta adalah pasar utama.** DKI Jakarta menyumbang hampir separuh GMV, terutama dari Jakarta Selatan dan Jakarta Pusat. Namun, di Desember pertumbuhan juga datang dari kota lain di Jakarta dan dari provinsi di luar lima besar.
3. **Customer belum loyal.** Sebagian besar customer DKI Jakarta di Q4 2019 hanya berbelanja sekali dan dalam jumlah kecil. Customer bernilai besar jumlahnya sedikit.
4. **Variasi produk lebih menentukan daripada harga.** Brand terlaris unggul karena memiliki banyak produk yang masing-masing terjual dalam jumlah sedang, bukan karena satu produk andalan atau harga yang murah.
5. **Promosi belum efisien.** Burn rate 2009-2012 selalu di atas target 4,5%, dan tidak diikuti kenaikan jumlah customer.
""")

st.header("Rekomendasi")
st.markdown("""
- Menyiapkan stok dan kampanye lebih awal menjelang kuartal keempat.
- Membuat program agar customer kembali berbelanja, misalnya voucher untuk pembelian kedua.
- Memperluas variasi produk pada brand yang potensial.
- Mengevaluasi besaran diskon agar burn rate kembali di bawah 4,5%.
""")
