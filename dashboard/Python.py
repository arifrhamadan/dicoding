import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
def load_data():
    # Sesuaikan path dataset sesuai lokasi file Anda
    day_data = pd.read_csv('./data/day.csv')
    hour_data = pd.read_csv('./data/hour.csv')
    return day_data, hour_data

# Main function to run the Streamlit app
def main():
    # Title of the dashboard
    st.title("Dashboard Analisis Data Peminjaman Sepeda")

    # Load data
    day_data, hour_data = load_data()

    # Sidebar for filtering
    st.sidebar.header("Filter")

    # Filter by season
    seasons = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    selected_season = st.sidebar.multiselect("Pilih Musim", options=list(seasons.keys()), format_func=lambda x: seasons[x])

    # Filter by date
    min_date = pd.to_datetime(day_data['dteday']).min()
    max_date = pd.to_datetime(day_data['dteday']).max()
    selected_date = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date])

    # Filter data
    filtered_day_data = day_data.copy()
    filtered_hour_data = hour_data.copy()

    if selected_season:
        filtered_day_data = filtered_day_data[filtered_day_data['season'].isin(selected_season)]
        filtered_hour_data = filtered_hour_data[filtered_hour_data['season'].isin(selected_season)]

    if selected_date:
        start_date, end_date = selected_date
        filtered_day_data['dteday'] = pd.to_datetime(filtered_day_data['dteday'])
        filtered_day_data = filtered_day_data[(filtered_day_data['dteday'] >= pd.Timestamp(start_date)) & (filtered_day_data['dteday'] <= pd.Timestamp(end_date))]
        
        filtered_hour_data['dteday'] = pd.to_datetime(filtered_hour_data['dteday'])
        filtered_hour_data = filtered_hour_data[(filtered_hour_data['dteday'] >= pd.Timestamp(start_date)) & (filtered_hour_data['dteday'] <= pd.Timestamp(end_date))]

    # Business Questions
    st.header("Pertanyaan Bisnis")
    st.write("1. Berapa distribusi peminjaman sepeda berdasarkan musim?")
    st.write("2. Bagaimana hubungan antara temperatur dan jumlah peminjaman sepeda?")

    # Data Visualizations
    st.header("Visualisasi Data")

    # Distribusi peminjaman sepeda berdasarkan musim
    st.subheader("Distribusi Peminjaman Sepeda Berdasarkan Musim")
    if not filtered_day_data.empty:
        plt.figure(figsize=(8, 6))
        season_counts = filtered_day_data.groupby('season')['cnt'].sum()
        season_counts.index = season_counts.index.map(seasons)
        plt.bar(season_counts.index, season_counts.values, color=['springgreen', 'skyblue', 'gold', 'tomato'])
        plt.title("Distribusi Peminjaman Sepeda Berdasarkan Musim")
        plt.xlabel("Musim")
        plt.ylabel("Jumlah Peminjaman")
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.warning("Data tidak ditemukan untuk filter yang dipilih.")

    # Hubungan temperatur dan jumlah peminjaman sepeda
    st.subheader("Hubungan Temperatur dan Jumlah Peminjaman Sepeda")
    if not filtered_hour_data.empty:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=filtered_hour_data, x='temp', y='cnt', alpha=0.6, color='blue')
        plt.title("Hubungan Temperatur dan Jumlah Peminjaman Sepeda")
        plt.xlabel("Temperatur")
        plt.ylabel("Jumlah Peminjaman")
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.warning("Data tidak ditemukan untuk filter yang dipilih.")

# Run the app
if __name__ == '__main__':
    main()
