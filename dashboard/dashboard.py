import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("dashboard/all_df.csv")

season_labels = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
weather_labels = {1: "Cerah", 2: "Mendung", 3: "Hujan"}

df["season_label"] = df["season_hour"].map(season_labels) 
df["weather_label"] = df["weathersit_hour"].map(weather_labels)

season_order = ["Gugur", "Panas", "Dingin", "Semi"]

weather_colors = {
    "Cerah": "#2E91E5",
    "Mendung": "#E15F99",
    "Hujan": "#1CA71C"
}

st.title("📊 Dashboard Analisis Penyewaan Sepeda 🚴")
st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim dan Kondisi Cuaca")

plt.figure(figsize=(10, 6))
bars = sns.barplot(
    x="season_label",
    y="cnt_day", 
    hue="weather_label",
    data=df,
    estimator=np.mean,
    palette=[weather_colors[w] for w in weather_labels.values()],
    order=season_order
)

plt.xlabel("Musim")
plt.ylabel("Rata-rata Penyewaan per Hari")
plt.title("Tren Penyewaan Sepeda Berdasarkan Musim dan Kondisi Cuaca")

for bar, label in zip(bars.patches, season_order * len(weather_labels)):
    if label == "Gugur":
        bar.set_facecolor("#B33E00")

plt.legend(title="Kondisi Cuaca")
st.pyplot(plt)

st.sidebar.subheader("🎛️ Filter Data")
selected_season = st.sidebar.multiselect("Pilih Musim:", season_order, default=season_order)
min_hour, max_hour = st.sidebar.slider("Rentang Jam:", 0, 23, (0, 23))

filtered_df = df[(df["season_label"].isin(selected_season)) & (df["hr"].between(min_hour, max_hour))]

st.subheader("⏰ Hubungan Jam Penyewaan dan Musim")

plt.figure(figsize=(12, 6))
sns.barplot(
    x="hr", 
    y="cnt_hour", 
    hue="season_label", 
    data=filtered_df, 
    estimator=np.mean, 
    order=range(24),
    palette="Set2"
)

plt.xlabel("Jam")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.title("Rata-rata Penyewaan Sepeda per Jam dalam Berbagai Musim")
plt.legend(title="Musim")
st.pyplot(plt)


st.subheader("🔍 Insight Berdasarkan Filter")

total_rentals = filtered_df["cnt_hour"].sum()
average_rentals = filtered_df["cnt_hour"].mean()


season_rentals = filtered_df.groupby("season_label")["cnt_hour"].sum().sort_values(ascending=False)
most_popular_season = season_rentals.idxmax() if not season_rentals.empty else "Tidak ada data"

hour_rentals = filtered_df.groupby("hr")["cnt_hour"].sum().sort_values(ascending=False)
peak_hour = hour_rentals.idxmax() if not hour_rentals.empty else "Tidak ada data"

st.write(f"""
📈 **Rata-rata Penyewaan Sepeda per Jam**: {average_rentals:.2f}  
🌦️ **Musim dengan Penyewaan Tertinggi dalam Rentang Waktu Ini**: {most_popular_season}  
⏰ **Jam dengan Penyewaan Tertinggi**: {peak_hour}:00  
""")

if most_popular_season == "Panas":
    st.write("🔥 Penyewaan meningkat signifikan saat musim panas, terutama di jam sibuk!")
elif most_popular_season == "Semi":
    st.write("🌸 Musim semi memiliki tren penyewaan yang stabil sepanjang hari.")
elif most_popular_season == "Gugur":
    st.write("🍂 Penyewaan di musim gugur cenderung stabil, tapi menurun setelah jam sibuk.")
elif most_popular_season == "Dingin":
    st.write("❄️ Musim dingin memiliki penyewaan yang lebih rendah, kemungkinan karena cuaca dingin.")
