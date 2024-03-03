import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.title('Dashboard Air Quality Dataset')

st.header('Kualitas Udara antara kota Chanping dan Kota Dongsi berdasarkan PM2.5 per bulan pada tahun 2013-2017')

chanping_df = pd.read_csv("https://drive.google.com/uc?id=1n9NqvkKY0Y9eMChWBdVKhH5gIMe_mT6t")
dongsi_df = pd.read_csv("https://drive.google.com/uc?id=1LT4j1PcDLT-OVP-3jsn9p6eZPsGZCaE_")

chanping_df.columns = chanping_df.columns.str.replace('PM2.5', 'PM25') 
dongsi_df.columns = dongsi_df.columns.str.replace('PM2.5', 'PM25') 

dongsi_df.PM25.fillna(value=dongsi_df.PM25.mean(), inplace=True)
dongsi_df.PM10.fillna(value=chanping_df.PM10.mean(), inplace=True)

chan = chanping_df.groupby(by='month').agg({
  'PM25':'mean'     
})

dong = dongsi_df.groupby(by='month').agg({
  'PM25':'mean'     
})


merge_df = pd.merge(
    left = chan,
    right = dong,
    how = "outer",
    left_on = "month",
    right_on = "month"
)

merge_df['bulan'] = range(1, 1 + len(merge_df))

merge_df.columns = merge_df.columns.str.replace('PM25_x', 'PM25 Kota Chanping') 
merge_df.columns = merge_df.columns.str.replace('PM25_y', 'PM25 Kota Dongsi') 

st.line_chart(
   merge_df, x="bulan", y=["PM25 Kota Chanping", "PM25 Kota Dongsi"], color=["#FF0000", "#0000FF"]  # Optional
)

st.subheader('Kualitas udara Kota Dongsin lebih buruk dibandingkan Kota Chanping Setiap awal tahun (januari dan februari) dan akhir tahun (oktober - desember) mengalami peningkatan signifikan diantara bulan lainnya ')
st.subheader('Saran : Warga Kota Chanping dan Kota Dongsi diharap untuk menggunakan masker pada waktu awal bulan dan akhir bulan serta untuk menanggulangi polusi diharap warga menggunakan kendaraan tidak bermotor apabila keperluannya tidak mendesak')

st.header('Hubungan Polusi PM2.5 dengan PM10 di Kota Dongsi pada tahun 2013-2017')


dongsi_pm25 = dongsi_df.groupby(by='month').agg({
  'PM25':'mean'     
})

dongsi_pm10 = dongsi_df.groupby(by='month').agg({
  'PM10':'mean'     
})

merge_df = pd.merge(
    left = dongsi_pm25,
    right = dongsi_pm10,
    how = "outer",
    left_on = "month",
    right_on = "month"
)

merge_df['bulan'] = range(1, 1 + len(merge_df))

st.scatter_chart(
    merge_df,
    x='PM25',
    y=["PM25","PM10"],
    color= ['#FF0000', '#0000FF']
)

st.scatter_chart(
    merge_df,
    x='PM10',
    y=["PM10","PM25"],
    color= [ '#0000FF','#FF0000']
)


st.subheader('hubungan antar polusi PM2.5 dan PM10 yaitu linier semakin tinggi polusi PM10 maka semakin tinggi juga tingkat polusi PM2.5 dibuktikan juga pada bagian exploretory tingkat korelasi menunjukkan 0.8 yaitu berhubungan kuat dan linier')
st.subheader('Saran : Untuk pemerintahan kota membuat regulasi bagaimana supaya tingkat polusi menurun')

