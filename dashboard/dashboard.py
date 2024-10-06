import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import calendar
import seaborn as sns


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
    return monthly_avg_rentals

day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

total=total_penyewa(day_df)
monthly_rentals = prepare_monthly_rentals(day_df)
monthly_avg_rentals = mothly_avg(day_df)

#Pie Chart Persentase Jumlah Penyewa Berdasarkan Status Keanggotaan
total_casual, total_registered = total
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
plt.title('Persentase Demografi Penyewa (2011 dan 2012)')
st.pyplot(fig)

# Membuat line chart
plt.figure(figsize=(10, 6))
for year in monthly_rentals['year'].unique():
    year_data = monthly_rentals[monthly_rentals['year'] == year]
    plt.plot(year_data['month'], 
            year_data['cnt'], 
            label=f'Tahun {year}', 
            marker='o', 
        linewidth=2
        )

plt.xticks(rotation=45)
plt.title('Total Penyewa Sepeda per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Total Penyewa')
plt.legend()
plt.tight_layout()
st.pyplot(plt)

#Tren
plt.figure(figsize=(10, 6))
sns.regplot(x='month_num', y='cnt', data=monthly_avg_rentals, marker='o', color='blue')
plt.xticks(ticks=range(1, 13), labels=list(calendar.month_name[1:]), rotation=45)
plt.title('Rata-Rata Jumlah Penyewa Sepeda per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Nilai Rata-Rata Penyewa')
st.pyplot(plt) 