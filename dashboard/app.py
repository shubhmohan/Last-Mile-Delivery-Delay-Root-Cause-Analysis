import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🚚 Delivery RCA Dashboard", layout="wide")

df=pd.read_csv("C:/Users/gupta\Documents/GitHub/Last-Mile-Delivery-Delay-Root-Cause-Analysis/data/processed/final_deliveries_clean.csv")

st.title("🚚 India Last-Mile Delivery — RCA Dashboard")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Delivery Time",  f"{df['Time_taken(min)'].mean():.1f} min")
col2.metric("On-Time Rate",       f"{df['On_Time'].mean()*100:.1f}%")
col3.metric("Total Deliveries",   f"{len(df):,}")
col4.metric("Avg Distance",       f"{df['Distance from Hub'].mean():.1f} km")

st.markdown("---")

# ── Sidebar Filters ───────────────────────────────────────
st.sidebar.header("🔍 Filters")
city    = st.sidebar.multiselect("City Type",    df['City'].unique(),            default=df['City'].unique())
traffic = st.sidebar.multiselect("Traffic Level", df['Road_traffic_density'].unique(), default=df['Road_traffic_density'].unique())
weather = st.sidebar.multiselect("Weather",       df['Weatherconditions'].unique(),    default=df['Weatherconditions'].unique())

filtered = df[
    df['City'].isin(city) &
    df['Road_traffic_density'].isin(traffic) &
    df['Weatherconditions'].isin(weather)
]

st.markdown(f"### Showing **{len(filtered):,}** deliveries after filters")

# ── Two charts side by side ───────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚦 Delay by Traffic Level")
    fig, ax = plt.subplots(figsize=(6, 4))
    order = ['Low','Medium','High','Jam']
    sns.barplot(x='Road_traffic_density', y='Time_taken(min)',
                data=filtered, order=order,
                hue='Road_traffic_density',
                palette=['#16A34A','#F59E0B','#EA580C','#EF4444'],
                legend=False, ax=ax)
    ax.set_xlabel("Traffic Level")
    ax.set_ylabel("Avg Time (min)")
    st.pyplot(fig)

with col2:
    st.subheader("🌦 Delay by Weather")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    weather_order = filtered.groupby('Weatherconditions')['Time_taken(min)']\
                            .mean().sort_values(ascending=False).index
    sns.barplot(x='Weatherconditions', y='Time_taken(min)',
                data=filtered, order=weather_order,
                hue='Weatherconditions', legend=False,
                palette='RdYlGn_r', ax=ax2)
    ax2.set_xlabel("Weather")
    ax2.set_ylabel("Avg Time (min)")
    plt.xticks(rotation=20)
    st.pyplot(fig2)

# ── What-If Simulator ─────────────────────────────────────
st.markdown("---")
st.subheader("🎛 What-If Simulator")
reduction = st.slider("If we reduce deliveries per courier by (orders):", 0, 3, 1)
sim = filtered.copy()
sim['Time_taken(min)'] = sim['Time_taken(min)'] - (reduction * 2.5)
current  = (filtered['On_Time'].mean() * 100)
improved = ((sim['Time_taken(min)'] <= sim['Time_taken(min)'].median()).mean() * 100)
st.success(f"✅ On-Time Rate: {current:.1f}% → {improved:.1f}% (+{improved-current:.1f}%)")