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
    "Artikel ini menyajikan analisis data transaksi DQLab Store dengan Python (pandas dan Matplotlib) "
    "dan SQL. Bagian 1-4 menganalisis transaksi Juli-Desember 2019, sedangkan Bagian 5 menganalisis "
    "kinerja penjualan dan promosi tahun 2009-2012."
)

# ------------------------------------------------------------------ BAGIAN 1
st.header("1. Tren GMV Bulanan 2019")

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
    "GMV relatif stabil pada Juli-September, lalu naik tajam di Oktober 2019 dan mencapai titik "
    "tertinggi di Desember."
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
st.write("Kesepuluh brand mencatat GMV kuartal keempat yang lebih tinggi dibanding kuartal ketiga.")

st.subheader("Gambar 3. Monthly GMV Year 2019 - Breakdown by Province")
plt.clf()
dataset.groupby(['order_month', 'province'])['gmv'].sum().unstack().plot(cmap='Set1')
plt.title('Monthly GMV Year 2019 - Breakdown by Province', loc='center', pad=30, fontsize=20, color='blue')
plt.xlabel('Order Month', fontsize=15)
plt.ylabel('Total Amount (in Billions)', fontsize=15)
plt.grid(color='darkgray', linestyle=':', linewidth=0.5)
plt.ylim(ymin=0)
labels, locations = plt.yticks()
plt.yticks(labels, (labels/1000000000).astype(int))
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), shadow=True, ncol=3, title='Province',
           fontsize=9, title_fontsize=11)
plt.gcf().set_size_inches(10, 5)
plt.tight_layout()
tampilkan()

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
    "DKI Jakarta mendominasi GMV di setiap bulan. Provinsi di luar lima besar (other) "
    "meningkat pesat di Desember 2019."
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
st.write("Jumlah customer harian di Desember 2019 berfluktuasi antara sekitar 19 dan 40 orang.")

# ------------------------------------------------------------------ BAGIAN 2
st.header("2. Fokus DKI Jakarta, Kuartal 4 2019")

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
        "Jakarta Selatan menyumbang porsi GMV terbesar di DKI Jakarta pada Q4 2019, "
        "diikuti Jakarta Pusat."
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
    "Jakarta Selatan mencatat GMV tertinggi di Oktober, sedangkan Jakarta Utara dan Jakarta Timur "
    "naik di Desember."
)

# ------------------------------------------------------------------ BAGIAN 3
st.header("3. Perilaku Customer DKI Jakarta Q4 2019")
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
    st.write("Sebagian besar customer (sekitar 500 orang) hanya melakukan satu kali order selama Q4 2019.")

st.subheader("Gambar 11. Distribution of Total Quantity per Customer")
plt.figure(figsize=(10, 5))
plt.hist(data_per_customer['quantity'], bins=100, range=(1, 200), color='brown')
plt.title('Distribution of Total Quantity per Customer\nDKI Jakarta in Q4 2019', fontsize=15, color='blue')
plt.xlabel('Quantity', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.xlim(xmin=0, xmax=200)
tampilkan()

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
st.write("Sebagian besar customer membeli dalam jumlah kecil dan dengan total GMV di bawah 25 juta.")

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
st.write("Quantity dan GMV per customer berkorelasi positif: makin banyak barang dibeli, makin besar GMV.")

# ------------------------------------------------------------------ BAGIAN 4
st.header("4. Top 5 Brand Desember 2019")

st.subheader("Tabel 1. Top 5 Brand Berdasarkan Quantity, Desember 2019")
st.dataframe(top_brands, hide_index=True)

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
st.write("BRAND_P mengalami lonjakan penjualan pada 9 Desember 2019, yaitu 312 unit dalam sehari.")

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
    "BRAND_S memiliki jumlah produk terjual terbanyak. Di semua brand, sebagian besar produk "
    "terjual kurang dari 100 unit selama Desember 2019."
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
st.write("Sebagian besar produk top 5 brand berharga di bawah 800 ribu, dengan puncak di 400-600 ribu.")

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
    "Quantity berkorelasi positif dengan GMV per produk, tetapi median harga hampir tidak berkorelasi "
    "dengan quantity: produk murah tidak selalu dibeli lebih banyak."
)

# ------------------------------------------------------------------ BAGIAN 5
st.header("5. Kinerja Penjualan dan Promosi 2009-2012 (SQL)")
st.write("Bagian ini menggunakan tabel `dqlab_sales_store`. Query dan hasilnya ditampilkan di bawah.")

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
st.write("Burn rate promosi di setiap tahun berada di atas target maksimum 4,5%.")

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
st.write("Jumlah customer yang bertransaksi relatif stabil di kisaran 580-595 per tahun.")

# ------------------------------------------------------------------ PENUTUP
st.header("Kesimpulan")
st.markdown("""
1. GMV DQLab Store naik tajam mulai Oktober 2019 dan memuncak di Desember 2019.
2. DKI Jakarta mendominasi GMV, dengan Jakarta Selatan sebagai kota penyumbang terbesar.
3. Sebagian besar customer DKI Jakarta di Q4 2019 hanya berbelanja sekali.
4. BRAND_S dan BRAND_P adalah brand dengan quantity terjual terbanyak di Desember 2019.
5. Burn rate promosi 2009-2012 selalu melebihi target 4,5%.
""")
