import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import calendar
sns.set(style='dark')

def rentals_total(df):
    total_all = df['cnt'].sum()
    return total_all

#Data Bike Rentals per Bulannya
def monthly_bike_rentals(df):
    # mengelompokkan data dan mengubah bulan menjadi nama bulan
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year'] = df['dteday'].dt.year
    df['month'] = df['dteday'].dt.month
    monthly_rentals = df.groupby(['year', 'month'])['cnt'].sum().reset_index()
    monthly_rentals['month'] = monthly_rentals['month'].apply(lambda x: calendar.month_name[x])
    monthly_rentals['month'] = pd.Categorical(monthly_rentals['month'], categories=list(calendar.month_name[1:]), ordered=True)
    
    #Rata-Rata Bike Rentals per Bulannya
    monthly_avg_rentals = monthly_rentals.groupby('month')['cnt'].mean().reset_index()
    monthly_avg_rentals['month_num'] = range(1, 13)
    
    # Mencari bulan dengan penyewa tertinggi untuk tahun 2011
    year_2011= monthly_rentals[monthly_rentals['year'] == 2011]
    highest_2011 =year_2011.loc[year_2011['cnt'].idxmax()]
    highest_bymonth_2011 = highest_2011['month']
    max_2011 = highest_2011['cnt']
    
    # Mencari bulan dengan penyewa tertinggi untuk tahun 2012
    year_2012= monthly_rentals[monthly_rentals['year'] == 2012]
    highest_2012 = year_2012.loc[year_2012['cnt'].idxmax()]
    highest_bymonth_2012 = highest_2012['month']
    max_2012 = highest_2012['cnt']
    
    return monthly_rentals, monthly_avg_rentals, highest_bymonth_2011, highest_bymonth_2012, max_2011, max_2012

def monthly_avg_byweather(df):
    weather_conditions = {
        1: 'Clear, Few clouds',
        2: 'Mist + Cloudy',
        3: 'Light Snow, Light Rain',
        4: 'Heavy Rain, Ice Pallets'
    }
    df['weather_desc'] = df['weathersit'].map(weather_conditions)
    weather_avg_rentals = df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_avg_rentals['weather_desc'] = weather_avg_rentals['weathersit'].map(weather_conditions)
    return weather_avg_rentals

def hourly_avg_rentals(df):
    hourly_avg = df.groupby("hr")["cnt"].mean().reset_index()
    return hourly_avg


# Load Data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Pendefinisian Fungsi
total = rentals_total(day_df)
monthly_rentals, monthly_avg_rentals, highest_bymonth_2011, highest_bymonth_2012, max_2011, max_2012 = monthly_bike_rentals(day_df)
weather_avg_rentals = monthly_avg_byweather(hour_df)
hourly = hourly_avg_rentals(hour_df)



st.header('Bike Rentals Dashboard :bike:')

# Sidebar
total_all = total
with st.sidebar:
    st.image("https://raw.githubusercontent.com/wahyunirosyidah/submission/main/dashboard/image.png")
    st.title("Everywhere, We Gowes!")
    st.metric("Total Bike Rentals", value=total_all)
    st.caption('Copyright © Wahyuni Fajrin Rosyidah 2024')


#Max Bike Rentals by Month
st.subheader('Monthly Bike Rentals (2011-2012)')
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
with col1:
    st.metric("Max Rentals by Month (2011)", value=highest_bymonth_2011)

with col2:
    st.metric("Max Rentals by Month (2012)", value=highest_bymonth_2012)

with col3:
    st.metric(f"Max Rentals in {highest_bymonth_2011} (2011)", value=max_2011)

with col4:
    st.metric(f"Max Rentals in {highest_bymonth_2012} (2012)", value=max_2012)

# Line Chart Max Bike Rentals by Month
plt.figure(figsize=(12, 7))
for year in monthly_rentals['year'].unique():
    year_data = monthly_rentals[monthly_rentals['year'] == year]
    plt.plot(year_data['month'],
             year_data['cnt'],
             label=f'Tahun {year}',
             marker='o',
             linewidth=2
             )

plt.xticks(rotation=45, fontsize=16)
plt.ylabel('Bike Rentals (Unit)', fontsize=20, labelpad=15)
plt.legend()
st.pyplot(plt)

# Regplot Average Bike Rentals by Month
st.subheader('Average Monthly Bike Rentals (2011-2012)')
plt.figure(figsize=(17, 8))
sns.regplot(x='month_num',
            y='cnt',
            data=monthly_avg_rentals, 
            marker='o',
            color='blue'
            )
plt.xticks(ticks=range(1, 13), labels=list(calendar.month_name[1:]), fontsize=16,rotation=45)
plt.xlabel("")
plt.ylabel('Average Bike Rentals (Unit)', fontsize=20, labelpad=15)
st.pyplot(plt)

# Bar Plot Average Rentals by Weather
st.subheader('Bike Rentals by Weather (2011-2012)')
plt.figure(figsize=(12, 7))
plt.bar(weather_avg_rentals['weather_desc'],
        weather_avg_rentals['cnt'],
        color='blue')
plt.xlabel('Weather', fontsize=16, labelpad=15)
plt.ylabel('Average Bike Rentals (Unit)', fontsize=16, labelpad=15)
st.pyplot(plt)


st.subheader('Hourly Bike Rentals (2011-2012)')
plt.figure(figsize=(10, 6))
plt.plot(hourly['hr'], 
         hourly['cnt'], 
         color='green')
plt.xlabel('Hour', fontsize=12, labelpad=15)
plt.ylabel('Average Bike Rentals (Unit)', fontsize=12, labelpad=15)

plt.xticks(range(0,24)) 

st.pyplot(plt)

