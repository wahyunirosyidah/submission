import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import calendar
sns.set(style='dark')

#Fungsi Menghitung total penyewa
def total_penyewa(df):
    total_casual = df['casual'].sum()
    total_registered = df['registered'].sum()
    return total_casual,total_registered

# Fungsi untuk mengelompokkan data dan mengubah bulan menjadi nama bulan
def prepare_monthly_rentals(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year'] = df['dteday'].dt.year
    df['month'] = df['dteday'].dt.month
    monthly_rentals = df.groupby(['year', 'month'])['cnt'].sum().reset_index()
    monthly_rentals['month'] = monthly_rentals['month'].apply(lambda x: calendar.month_name[x])
    monthly_rentals['month'] = pd.Categorical(monthly_rentals['month'], categories=list(calendar.month_name[1:]), ordered=True)
    return monthly_rentals

def mothly_avg(df):
    monthly_rentals = df.groupby(['year', 'month'])['cnt'].sum().reset_index()
    monthly_avg_rentals = monthly_rentals.groupby('month')['cnt'].mean().reset_index()
    monthly_avg_rentals['month_num'] = range(1, 13)
    
    day_df['year'] = day_df['dteday'].dt.year
    year_2011 = monthly_rentals[monthly_rentals['year'] == 2011]
    year_2012 = monthly_rentals[monthly_rentals['year'] == 2012]
    
    highest_2011 = monthly_rentals[monthly_rentals['year'] == 2011].loc[monthly_rentals[monthly_rentals['year'] == 2011]['cnt'].idxmax()]
    highest_bymonth_2011 = calendar.month_name[int(highest_2011['month'])]
    max_2011 = highest_2011['cnt']

    highest_2012 = monthly_rentals[monthly_rentals['year'] == 2012].loc[monthly_rentals[monthly_rentals['year'] == 2012]['cnt'].idxmax()]
    highest_bymonth_2012 = calendar.month_name[int(highest_2012['month'])]
    max_2012 = highest_2012['cnt']

    
    return monthly_avg_rentals,highest_bymonth_2011,highest_bymonth_2012,max_2011,max_2012,year_2011,year_2012

def monthly_avg_byweather(df):
    weather_conditions = {
    1: 'Clear, Few clouds',
    2: 'Mist + Cloudy',
    3: 'Light Snow, Light Rain',
    4: 'Heavy Rain, Ice Pallets'
    }
    hour_df['weather_desc'] =df['weathersit'].map(weather_conditions)
    weather_avg_rentals = df.groupby('weathersit')['cnt'].mean().reset_index()
    weather_avg_rentals['weather_desc'] = weather_avg_rentals['weathersit'].map(weather_conditions)
    return weather_avg_rentals



day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

total=total_penyewa(day_df)
monthly_rentals = prepare_monthly_rentals(day_df)
# monthly_avg_rentals = mothly_avg(day_df)
weather_avg_rentals = monthly_avg_byweather(hour_df)

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    



#Pie Chart Persentase Jumlah Penyewa Berdasarkan Status Keanggotaan
total_casual, total_registered = total
st.subheader('Bike Rentals Demographics by Membership Status (2011-2012)')
#Kolom Data
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Registered User", value=total_registered)

with col2:
    st.metric("Total Casual Users", value=total_casual)

#Pie Chart
colors = ['#F4D06F', '#73E2A7']
explode = (0.1, 0)

fig, ax = plt.subplots()
ax.pie(
    x=(total_registered, total_casual),
    labels=('Registered', 'Casual'),
    autopct='%1.1f%%',
    colors=colors,
    explode=explode,
    startangle=90
)
ax.axis('equal') 
st.pyplot(fig)

# Membuat line chart
monthly_avg_rentals, highest_bymonth_2011, highest_bymonth_2012, max_2011, max_2012, year_2011,year_2012=mothly_avg(day_df)
st.subheader('Monthly Bike Rentals (2011-2012)')
col5,col6 = st.columns(2)
col7, col8= st.columns(2)
with col5:
    st.metric("Max Rentals by Month(2011)", value=highest_bymonth_2011)

with col6:
    st.metric("Max Rental by Month(2012)", value=highest_bymonth_2012)

with col7:
    st.metric(f"Max Rentals {highest_bymonth_2011} (2011)", value=max_2011)

with col8:
    st.metric(f"Max Rentals {highest_bymonth_2012} (2012)", value=max_2012)    
    
plt.figure(figsize=(12, 7))
for year in monthly_rentals['year'].unique():
    year_data = monthly_rentals[monthly_rentals['year'] == year]
    plt.plot(year_data['month'], 
            year_data['cnt'], 
            label=f'Tahun {year}', 
            marker='o', 
        linewidth=2
        )


plt.ylabel('Total Penyewa', fontsize=20,labelpad=15)
plt.legend()
plt.tight_layout()
st.pyplot(plt)

#Tren
plt.figure(figsize=(17,8))
sns.regplot(x='month_num', 
            y='cnt', 
            data=monthly_avg_rentals, 
            marker='o', 
            color='blue'
            )
plt.xticks(ticks=range(1, 13), labels=list(calendar.month_name[1:]),fontsize=16)
plt.xlabel("")
plt.ylabel('Jumlah Rata-Rata Penyewa', fontsize=20,labelpad=15)
st.pyplot(plt) 


#Bar Plot
st.subheader('Average Bike Rentals by Weather (2011-2012)')
plt.figure(figsize=(12, 7))
plt.bar(weather_avg_rentals['weather_desc'], 
        weather_avg_rentals['cnt'], 
        color='blue')
plt.xlabel('Kondisi Cuaca', fontsize=16,labelpad=15)
plt.ylabel('Rata-Rata Jumlah Penyewa', fontsize=16,labelpad=15)
st.pyplot(plt)

def prepare_monthly_rentals_with_weather(df):
    # Konversi kolom 'dteday' ke tipe datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Ekstrak tahun dan bulan dari 'dteday'
    df['year'] = df['dteday'].dt.year
    df['month'] = df['dteday'].dt.month

    # Kelompokkan data berdasarkan tahun dan bulan
    monthly_rentals = df.groupby(['year', 'month']).agg({
        'cnt': 'sum',               # Total penyewa
        'weathersit': lambda x: x.mode()[0]  # Cuaca yang paling sering muncul
    }).reset_index()

    return monthly_rentals


# Fungsi untuk mendapatkan cuaca paling sering dalam format nama
def get_weather_name(weathersit_value):
    weather_dict = {
    1: 'Clear, Few clouds',
    2: 'Mist + Cloudy',
    3: 'Light Snow, Light Rain',
    4: 'Heavy Rain, Ice Pallets'
    }
    return weather_dict.get(weathersit_value, "Tidak diketahui")



# Mendapatkan data penyewaan dan cuaca paling sering per bulan
monthly_rentals_with_weather = prepare_monthly_rentals_with_weather(day_df)

# Menyiapkan data per tahun
rentals_2011 = monthly_rentals_with_weather[monthly_rentals_with_weather['year'] == 2011]
rentals_2012 = monthly_rentals_with_weather[monthly_rentals_with_weather['year'] == 2012]

# Membuat tabel untuk tahun 2011
st.subheader('Cuaca Tersering per Bulan (2011)')
table_2011 = rentals_2011.copy()
table_2011['month'] = table_2011['month'].apply(lambda x: calendar.month_name[x])
table_2011['weathersit'] = table_2011['weathersit'].apply(get_weather_name)
table_2011 = table_2011[['month', 'weathersit']]  # Hanya menampilkan kolom bulan dan cuaca tersering
st.table(table_2011.rename(columns={"month": "Bulan", "weathersit": "Cuaca Tersering"}))

# Membuat tabel untuk tahun 2012
st.subheader('Cuaca Tersering per Bulan (2012)')
table_2012 = rentals_2012.copy()
table_2012['month'] = table_2012['month'].apply(lambda x: calendar.month_name[x])
table_2012['weathersit'] = table_2012['weathersit'].apply(get_weather_name)
table_2012 = table_2012[['month', 'weathersit']]  # Hanya menampilkan kolom bulan dan cuaca tersering
st.table(table_2012.rename(columns={"month": "Bulan", "weathersit": "Cuaca Tersering"}))
