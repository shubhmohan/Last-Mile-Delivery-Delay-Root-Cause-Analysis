import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from scipy import stats

st.set_page_config(
    page_title="🚚 India Delivery RCA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0F172A; }
    .block-container { padding-top: 1rem; }

    .kpi-card {
        background: linear-gradient(135deg, #1E293B, #0F2040);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border-left: 4px solid;
        margin: 4px;
    }
    .kpi-value { font-size: 2rem; font-weight: 800; margin: 0; }
    .kpi-label { font-size: 0.8rem; color: #94A3B8; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-delta { font-size: 0.75rem; margin-top: 4px; }

    .section-header {
        background: linear-gradient(90deg, #0D9488, #0F2040);
        padding: 10px 16px;
        border-radius: 8px;
        color: white;
        font-weight: 700;
        font-size: 1rem;
        margin: 16px 0 8px 0;
    }
    .insight-box {
        background: #1E293B;
        border-left: 4px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        color: #E2E8F0;
        font-size: 0.9rem;
        margin: 8px 0;
    }
    .rca-env  { border-left-color: #0D9488 !important; }
    .rca-ops  { border-left-color: #F59E0B !important; }
    .rca-beh  { border-left-color: #EF4444 !important; }
    .rca-str  { border-left-color: #A78BFA !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# LOAD & CLEAN DATA
# ══════════════════════════════════════════════
@st.cache_data
def load_data():
    df=pd.read_csv("C:/Users/gupta\Documents/GitHub/Last-Mile-Delivery-Delay-Root-Cause-Analysis/data/processed/final_deliveries_clean.csv")

    # Clean text columns
    df['Weatherconditions']    = df['Weatherconditions'].str.replace('conditions ', '', regex=False).str.strip()
    df['Road_traffic_density'] = df['Road_traffic_density'].str.strip()
    df['City']                 = df['City'].str.strip()
    df['Festival']             = df['Festival'].str.strip()
    df['Experience']           = df['Experience'].str.strip()

    # Drop NaN weather
    df = df[~df['Weatherconditions'].isin(['NaN', 'nan'])]
    df = df.dropna(subset=['Weatherconditions', 'Road_traffic_density'])
    df = df[df['City'].notna()]
    df = df[df['City'] != 'NaN']

    # Ensure numeric
    df['Time_taken(min)']        = pd.to_numeric(df['Time_taken(min)'],        errors='coerce')
    df['Distance from Hub']      = pd.to_numeric(df['Distance from Hub'],      errors='coerce')
    df['Delivery_person_Ratings']= pd.to_numeric(df['Delivery_person_Ratings'],errors='coerce')
    df['Delivery_person_Age']    = pd.to_numeric(df['Delivery_person_Age'],    errors='coerce')
    df['multiple_deliveries']    = pd.to_numeric(df['multiple_deliveries'],    errors='coerce')

    df = df.dropna(subset=['Time_taken(min)'])
    return df

df = load_data()

# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔍 Dashboard Filters")
    st.markdown("---")

    city_opts = sorted(df['City'].dropna().unique())
    city = st.multiselect("🏙 City Type", city_opts, default=city_opts)

    traffic_order = ['Low', 'Medium', 'High', 'Jam']
    traffic_opts  = [t for t in traffic_order if t in df['Road_traffic_density'].unique()]
    traffic = st.multiselect("🚦 Traffic Level", traffic_opts, default=traffic_opts)

    weather_opts = sorted(df['Weatherconditions'].dropna().unique())
    weather = st.multiselect("🌦 Weather", weather_opts, default=weather_opts)

    festival = st.radio("🎉 Festival Period", ["All", "Yes", "No"])

    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    st.markdown(f"**Total rows:** {len(df):,}")
    st.markdown(f"**Unique couriers:** {df['Delivery_person_ID'].nunique():,}")
    st.markdown(f"**Cities:** {df['City'].nunique()}")

# ── Apply filters ─────────────────────────────
filtered = df[
    df['City'].isin(city) &
    df['Road_traffic_density'].isin(traffic) &
    df['Weatherconditions'].isin(weather)
]
if festival != "All":
    filtered = filtered[filtered['Festival'] == festival]

# ══════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div style='background: linear-gradient(135deg, #0F2040, #0D9488);
     padding: 20px 28px; border-radius: 12px; margin-bottom: 16px;'>
    <h1 style='color: white; margin: 0; font-size: 1.8rem;'>
        🚚 India Last-Mile Delivery — RCA Dashboard
    </h1>
    <p style='color: #94A3B8; margin: 4px 0 0 0; font-size: 0.9rem;'>
        Root Cause Analysis  |  45,000+ Real Deliveries  |  India Operations
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"📦 Showing **{len(filtered):,}** deliveries after filters")

# ══════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════
k1, k2, k3, k4, k5 = st.columns(5)

avg_time    = filtered['Time_taken(min)'].mean()
ontime_rate = filtered['On_Time'].mean() * 100
total       = len(filtered)
avg_dist    = filtered['Distance from Hub'].mean()
avg_rating  = filtered['Delivery_person_Ratings'].mean()

k1.markdown(f"""<div class='kpi-card' style='border-left-color:#0D9488'>
    <p class='kpi-label'>Avg Delivery Time</p>
    <p class='kpi-value' style='color:#0D9488'>{avg_time:.1f}</p>
    <p class='kpi-delta' style='color:#94A3B8'>minutes</p>
</div>""", unsafe_allow_html=True)

k2.markdown(f"""<div class='kpi-card' style='border-left-color:#16A34A'>
    <p class='kpi-label'>On-Time Rate</p>
    <p class='kpi-value' style='color:#16A34A'>{ontime_rate:.1f}%</p>
    <p class='kpi-delta' style='color:#94A3B8'>of deliveries</p>
</div>""", unsafe_allow_html=True)

k3.markdown(f"""<div class='kpi-card' style='border-left-color:#F59E0B'>
    <p class='kpi-label'>Total Deliveries</p>
    <p class='kpi-value' style='color:#F59E0B'>{total:,}</p>
    <p class='kpi-delta' style='color:#94A3B8'>filtered records</p>
</div>""", unsafe_allow_html=True)

k4.markdown(f"""<div class='kpi-card' style='border-left-color:#A78BFA'>
    <p class='kpi-label'>Avg Distance</p>
    <p class='kpi-value' style='color:#A78BFA'>{avg_dist:.1f}</p>
    <p class='kpi-delta' style='color:#94A3B8'>km from hub</p>
</div>""", unsafe_allow_html=True)

k5.markdown(f"""<div class='kpi-card' style='border-left-color:#EF4444'>
    <p class='kpi-label'>Avg Courier Rating</p>
    <p class='kpi-value' style='color:#EF4444'>{avg_rating:.2f}</p>
    <p class='kpi-delta' style='color:#94A3B8'>out of 6.0</p>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# ROW 1 — Traffic + Weather
# ══════════════════════════════════════════════
st.markdown("<div class='section-header'>📊 Phase A — Descriptive Analysis</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🚦 Avg Delivery Time by Traffic Level")
    t_order = [t for t in ['Low','Medium','High','Jam'] if t in filtered['Road_traffic_density'].unique()]
    t_data  = filtered.groupby('Road_traffic_density')['Time_taken(min)'].mean().reindex(t_order)

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor('#1E293B')
    ax.set_facecolor('#1E293B')

    colors  = ['#16A34A','#F59E0B','#EA580C','#EF4444'][:len(t_order)]
    bars    = ax.bar(t_order, t_data.values, color=colors, edgecolor='none', width=0.55)

    for bar, val in zip(bars, t_data.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{val:.1f} min', ha='center', va='bottom',
                color='white', fontsize=11, fontweight='bold')

    ax.set_xlabel('Traffic Level', color='#94A3B8', fontsize=11)
    ax.set_ylabel('Avg Time (min)', color='#94A3B8', fontsize=11)
    ax.tick_params(colors='#CBD5E1')
    ax.spines[['top','right','left','bottom']].set_visible(False)
    ax.yaxis.grid(True, color='#334155', linewidth=0.5)
    ax.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("<div class='insight-box rca-env'>🔍 <b>Finding:</b> Jam traffic adds <b>~10 extra minutes</b> vs Low traffic. Invest in routing AI, not more riders.</div>", unsafe_allow_html=True)

with col2:
    st.markdown("#### 🌦 Avg Delivery Time by Weather")
    w_data = filtered.groupby('Weatherconditions')['Time_taken(min)'].mean().sort_values(ascending=False)

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    fig2.patch.set_facecolor('#1E293B')
    ax2.set_facecolor('#1E293B')

    w_colors = ['#EF4444' if v > filtered['Time_taken(min)'].mean() else '#16A34A' for v in w_data.values]
    bars2 = ax2.bar(w_data.index, w_data.values, color=w_colors, edgecolor='none', width=0.55)

    for bar, val in zip(bars2, w_data.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f'{val:.1f}', ha='center', va='bottom',
                 color='white', fontsize=10, fontweight='bold')

    ax2.axhline(y=filtered['Time_taken(min)'].mean(), color='#F59E0B',
                linestyle='--', linewidth=1.5, label=f'Fleet avg: {filtered["Time_taken(min)"].mean():.1f} min')
    ax2.legend(facecolor='#1E293B', labelcolor='white', fontsize=9)
    ax2.set_xlabel('Weather Condition', color='#94A3B8', fontsize=11)
    ax2.set_ylabel('Avg Time (min)', color='#94A3B8', fontsize=11)
    ax2.tick_params(colors='#CBD5E1', rotation=20)
    ax2.spines[['top','right','left','bottom']].set_visible(False)
    ax2.yaxis.grid(True, color='#334155', linewidth=0.5)
    ax2.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig2)
    st.markdown("<div class='insight-box rca-env'>🔍 <b>Finding:</b> Fog/Cloudy adds <b>+7 min</b> vs Sunny. Festival periods add <b>+4 min</b>. Confirms 🌧 Environmental bucket.</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# ROW 2 — City violin + Multiple deliveries
# ══════════════════════════════════════════════
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🏙 Delivery Time Distribution by City")
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    fig3.patch.set_facecolor('#1E293B')
    ax3.set_facecolor('#1E293B')

    city_palette = {'Metropolitian': '#0D9488', 'Urban': '#F59E0B', 'Semi-Urban': '#EF4444'}
    city_in_data = [c for c in ['Metropolitian','Urban','Semi-Urban'] if c in filtered['City'].unique()]
    sns.violinplot(x='City', y='Time_taken(min)', data=filtered,
                   order=city_in_data,
                   palette=city_palette, ax=ax3, inner='quartile')

    ax3.set_xlabel('City Type', color='#94A3B8', fontsize=11)
    ax3.set_ylabel('Delivery Time (min)', color='#94A3B8', fontsize=11)
    ax3.tick_params(colors='#CBD5E1')
    ax3.spines[['top','right','left','bottom']].set_visible(False)
    ax3.yaxis.grid(True, color='#334155', linewidth=0.5)
    plt.tight_layout()
    st.pyplot(fig3)
    st.markdown("<div class='insight-box rca-str'>🔍 <b>Finding:</b> Semi-Urban has widest spread — structural address issues. Metropolitan = most consistent.</div>", unsafe_allow_html=True)

with col4:
    st.markdown("#### 📦 Impact of Multiple Deliveries per Trip")
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    fig4.patch.set_facecolor('#1E293B')
    ax4.set_facecolor('#1E293B')

    md_data   = filtered.groupby('multiple_deliveries')['Time_taken(min)'].mean().sort_index()
    md_colors = ['#16A34A','#F59E0B','#EA580C','#EF4444'][:len(md_data)]
    bars4 = ax4.bar(md_data.index.astype(str), md_data.values,
                    color=md_colors, edgecolor='none', width=0.5)

    for bar, val in zip(bars4, md_data.values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f'{val:.1f} min', ha='center', va='bottom',
                 color='white', fontsize=11, fontweight='bold')

    ax4.set_xlabel('Number of Deliveries per Trip', color='#94A3B8', fontsize=11)
    ax4.set_ylabel('Avg Time (min)', color='#94A3B8', fontsize=11)
    ax4.tick_params(colors='#CBD5E1')
    ax4.spines[['top','right','left','bottom']].set_visible(False)
    ax4.yaxis.grid(True, color='#334155', linewidth=0.5)
    ax4.set_axisbelow(True)
    plt.tight_layout()
    st.pyplot(fig4)
    st.markdown("<div class='insight-box rca-ops'>🔍 <b>Finding:</b> multiple_deliveries is the <b>#1 delay driver (r=0.38)</b>. Fix order batching at dispatch level.</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# ROW 3 — Z-Score + Ratings scatter
# ══════════════════════════════════════════════
st.markdown("<div class='section-header'>🔬 Phase B — Diagnostic Analysis</div>", unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("#### 👤 Courier Z-Score Distribution")

    courier_avg = filtered.groupby('Delivery_person_ID')['Time_taken(min)'].mean()
    z_scores    = (courier_avg - courier_avg.mean()) / courier_avg.std()
    n_outliers  = (z_scores > 3).sum()
    n_top       = (z_scores < -1).sum()

    fig5, ax5 = plt.subplots(figsize=(7, 4))
    fig5.patch.set_facecolor('#1E293B')
    ax5.set_facecolor('#1E293B')

    ax5.hist(z_scores, bins=35, color='#0D9488', edgecolor='#0F172A', alpha=0.85)
    ax5.axvline(x=3,  color='#EF4444', linestyle='--', linewidth=2, label=f'Outlier threshold Z=3 ({n_outliers} couriers)')
    ax5.axvline(x=-1, color='#16A34A', linestyle='--', linewidth=2, label=f'Top performers Z<-1 ({n_top} couriers)')
    ax5.axvline(x=0,  color='#F59E0B', linestyle='-',  linewidth=1, label='Fleet average')
    ax5.legend(facecolor='#1E293B', labelcolor='white', fontsize=9)
    ax5.set_xlabel('Z-Score', color='#94A3B8', fontsize=11)
    ax5.set_ylabel('Number of Couriers', color='#94A3B8', fontsize=11)
    ax5.tick_params(colors='#CBD5E1')
    ax5.spines[['top','right','left','bottom']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig5)

    c1, c2 = st.columns(2)
    c1.metric("⚠ Outlier Couriers (Z>3)", n_outliers, delta="Need retraining", delta_color="inverse")
    c2.metric("⭐ Top Performers (Z<-1)", n_top, delta="Benchmark these")

with col6:
    st.markdown("#### ⭐ Courier Rating vs Delivery Time")
    fig6, ax6 = plt.subplots(figsize=(7, 4))
    fig6.patch.set_facecolor('#1E293B')
    ax6.set_facecolor('#1E293B')

    rating_data = filtered.groupby('Delivery_person_Ratings')['Time_taken(min)'].mean().reset_index()
    ax6.scatter(rating_data['Delivery_person_Ratings'], rating_data['Time_taken(min)'],
                color='#0D9488', s=80, alpha=0.8, zorder=3)

    # Trend line
    z = np.polyfit(rating_data['Delivery_person_Ratings'], rating_data['Time_taken(min)'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(rating_data['Delivery_person_Ratings'].min(),
                          rating_data['Delivery_person_Ratings'].max(), 100)
    ax6.plot(x_line, p(x_line), color='#EF4444', linewidth=2, linestyle='--', label='Trend line')

    ax6.legend(facecolor='#1E293B', labelcolor='white', fontsize=9)
    ax6.set_xlabel('Courier Rating', color='#94A3B8', fontsize=11)
    ax6.set_ylabel('Avg Delivery Time (min)', color='#94A3B8', fontsize=11)
    ax6.tick_params(colors='#CBD5E1')
    ax6.spines[['top','right','left','bottom']].set_visible(False)
    ax6.yaxis.grid(True, color='#334155', linewidth=0.5)
    plt.tight_layout()
    st.pyplot(fig6)
    st.markdown("<div class='insight-box rca-beh'>🔍 <b>Finding:</b> Higher rated couriers deliver faster (r=-0.32). Gamification & incentives directly reduce delivery time.</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# RCA BUCKET SUMMARY
# ══════════════════════════════════════════════
st.markdown("<div class='section-header'>🎯 RCA Bucket Summary — Root Causes Identified</div>", unsafe_allow_html=True)

b1, b2, b3, b4 = st.columns(4)

jam_avg   = filtered[filtered['Road_traffic_density']=='Jam']['Time_taken(min)'].mean()
low_avg   = filtered[filtered['Road_traffic_density']=='Low']['Time_taken(min)'].mean()
fog_avg   = filtered[filtered['Weatherconditions'].isin(['Fog','Cloudy'])]['Time_taken(min)'].mean()
sunny_avg = filtered[filtered['Weatherconditions']=='Sunny']['Time_taken(min)'].mean()

b1.markdown(f"""<div class='insight-box rca-env' style='min-height:120px'>
<b>🌧 Environmental</b><br>
Fog/Cloudy adds <b>+{fog_avg - sunny_avg:.1f} min</b><br>
Jam vs Low traffic: <b>+{jam_avg - low_avg:.1f} min</b><br>
<br><i>Fix: Dynamic promised time + IMD API</i>
</div>""", unsafe_allow_html=True)

md_0 = filtered[filtered['multiple_deliveries']==0]['Time_taken(min)'].mean() if 0 in filtered['multiple_deliveries'].values else 0
md_2 = filtered[filtered['multiple_deliveries']==2]['Time_taken(min)'].mean() if 2 in filtered['multiple_deliveries'].values else 0

b2.markdown(f"""<div class='insight-box rca-ops' style='min-height:120px'>
<b>🏭 Operational</b><br>
Multiple deliveries = <b>#1 driver (r=0.38)</b><br>
2 orders vs 0: <b>+{md_2 - md_0:.1f} min</b><br>
<br><i>Fix: Smarter order batching at dispatch</i>
</div>""", unsafe_allow_html=True)

b3.markdown(f"""<div class='insight-box rca-beh' style='min-height:120px'>
<b>👤 Behavioural</b><br>
Outlier couriers: <b>{n_outliers}</b> (Z > 3)<br>
Rating r = <b>-0.32</b> with delivery time<br>
<br><i>Fix: Gamification + retraining program</i>
</div>""", unsafe_allow_html=True)

semi_avg  = filtered[filtered['City']=='Semi-Urban']['Time_taken(min)'].mean() if 'Semi-Urban' in filtered['City'].values else 0
metro_avg = filtered[filtered['City']=='Metropolitian']['Time_taken(min)'].mean() if 'Metropolitian' in filtered['City'].values else 0

b4.markdown(f"""<div class='insight-box rca-str' style='min-height:120px'>
<b>🏗 Structural</b><br>
Semi-Urban vs Metro: <b>+{semi_avg - metro_avg:.1f} min</b><br>
Age r = <b>+0.29</b> with delivery time<br>
<br><i>Fix: Update ETA model + landmark field</i>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# WHAT-IF SIMULATOR
# ══════════════════════════════════════════════
st.markdown("<div class='section-header'>🎛 What-If Simulator — Business Decision Tool</div>", unsafe_allow_html=True)

sim_col1, sim_col2 = st.columns([1, 1])

with sim_col1:
    st.markdown("#### Adjust Operational Parameters")
    reduce_orders  = st.slider("📦 Reduce orders per courier by:", 0, 2, 0,
                                help="Reducing multiple deliveries per trip")
    reduce_traffic = st.slider("🚦 Routing AI improvement (min saved in Jam):", 0, 10, 0,
                                help="Minutes saved through better routing")
    improve_rating = st.slider("⭐ Courier training: rating improvement:", 0.0, 1.0, 0.0, step=0.1,
                                help="Avg rating increase through gamification")

with sim_col2:
    st.markdown("#### 📈 Projected Impact")
    sim = filtered.copy()

    # Apply simulations
    time_saved = (reduce_orders * 2.8) + (reduce_traffic * 0.6) + (improve_rating * 1.5)
    sim['Simulated_Time'] = sim['Time_taken(min)'] - time_saved
    sim['Simulated_OnTime'] = (sim['Simulated_Time'] <= sim['Time_taken(min)'].median()).astype(int)

    current_ontime  = filtered['On_Time'].mean() * 100
    simulated_ontime= sim['Simulated_OnTime'].mean() * 100
    improvement     = simulated_ontime - current_ontime
    time_reduction  = time_saved

    m1, m2, m3 = st.columns(3)
    m1.metric("Current On-Time",    f"{current_ontime:.1f}%")
    m2.metric("Projected On-Time",  f"{simulated_ontime:.1f}%",
              delta=f"+{improvement:.1f}%", delta_color="normal")
    m3.metric("Avg Time Saved",     f"{time_reduction:.1f} min",
              delta="per delivery", delta_color="normal")

    if time_saved > 0:
        st.success(f"✅ By reducing courier load by {reduce_orders} orders, improving routing by {reduce_traffic} min, and raising ratings by {improve_rating:.1f} — on-time rate improves by **{improvement:.1f}%**")
    else:
        st.info("👆 Move the sliders above to simulate operational improvements")

# ══════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#475569; font-size:0.8rem; padding: 10px'>
    🚚 India Last-Mile Delivery RCA Dashboard  |  Data: Kaggle Food Delivery Dataset (45,593 rows)  |  Built with Streamlit + Seaborn
</div>
""", unsafe_allow_html=True)