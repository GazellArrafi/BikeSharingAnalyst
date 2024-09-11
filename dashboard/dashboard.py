import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

#Perhitungan
def get_total_count_by_hour_df(hour_df):
    hour_count_df =  hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
    return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
    reg_df =  day_df.groupby(by="dteday").agg({
        "registered": "sum"
    })
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
    return reg_df

def total_casual_df(day_df):
    cas_df =  day_df.groupby(by="dteday").agg({
        "casual": ["sum"]
    })
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
    return cas_df

def sum_order_hourly (hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def sum_ordeer_hourly_peak(hour_df):
    sum_order_items_df1 = hour_df.groupby("hours").agg({
        "casual": "sum",
        "registered": "sum",
        "count_cr": "sum"
    }).reset_index()
    return sum_order_items_df1

def get_daily_users(day_df):
    daily_users_df = day_df.groupby(by="a_week").count_cr.sum().reset_index()
    return daily_users_df
    
def all_season (day_df): 
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index() 
    return season_df

days_df = pd.read_csv("dashboard/newDay_df.csv", sep=";")
hours_df = pd.read_csv("dashboard/newHour_df.csv", sep=";")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)  
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column], dayfirst=True)
    hours_df[column] = pd.to_datetime(hours_df[column], dayfirst=True)

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    # Logo
    st.image("https://cdn0-production-images-kly.akamaized.net/lSS8-UqhLuKdFHWIgBK_oz7yCjs=/1280x720/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3169550/original/034953400_1593770747-20200703-Pemprov-DKI-Akan-Sediakan-Layanan-Bike-Sharing-angga-2.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                        (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

#Penggunaan Function
hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order_hourly(main_df_hour)
sum_ordeer_hourly_peak_df = sum_ordeer_hourly_peak(main_df_hour)
daily_users_df = get_daily_users(days_df)
season_df = all_season(main_df_hour)

#Dashboard
st.header('Dashboard enyewaan Sepeda :sparkles:')
st.subheader('Perhitungan penyewaan Sepeda')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total penyewa sepeda", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total penyewa yang registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total penyewa yang casual", value=total_sum)

#Pertanyaan 1
st.subheader("Jam berapa yang mencatatkan jumlah penyewaan sepeda terbanyak dan terendah?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

plt.figure(figsize=(16,6))

st.pyplot(fig)

#Pertanyaan 2
st.subheader("Pada jam berapa saja terjadinya lonjakan kenaikan penyewaan sepeda?")
fig, ax = plt.subplots(figsize=(16, 6))

sns.lineplot(x="hours", y="casual", data=sum_ordeer_hourly_peak_df, label='Casual', ax=ax)
sns.lineplot(x="hours", y="registered", data=sum_ordeer_hourly_peak_df, label='Registered', ax=ax)

x = np.arange(0, 24, 1)
ax.set_xticks(x)

ax.axvline(x=8, color='black', linestyle='--')
ax.axvline(x=17, color='black', linestyle='--')

ax.legend(loc='upper right', fontsize=14)
ax.set_xlabel("Jam", fontsize=14)
ax.set_ylabel("Total Penyewa", fontsize=14)
ax.set_title("Jumlah penyewa per jam", fontsize=16)

st.pyplot(fig)

#Pertanyaan 3
st.subheader("Hari apa yang memiliki jumlah penyewaan sepeda tertinggi?")
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x="a_week", y="count_cr", data=daily_users_df, 
            palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"],
            order=["Monday", "Tuesday", "Wednesday", "Thrusday", "Friday", "Saturday", "Sunday"], 
            ax=ax)

ax.set_xlabel("Hari", fontsize=14)
ax.set_ylabel("Total Penyewa", fontsize=14)
ax.set_title("Jumlah Penyewa per Hari", fontsize=16)

st.pyplot(fig)

#pertanyaan 4
st.subheader("Musim apa yang memiliki jumlah penyewaan sepeda tertinggi?")

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        y="count_cr", 
        x="season",
        data=season_df.sort_values(by="season", ascending=False),
        palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"],
        ax=ax
    )
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

#pertanyaan 5
st.subheader("Berapa banyak orang yang menjadi 'registered' dibandingkan dengan 'casual' dalam hal penyewaan sepeda?")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)
