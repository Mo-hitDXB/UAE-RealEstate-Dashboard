import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="UAE Real Estate Dashboard",
    layout="wide"
)

# =====================================================
# GLOBAL CSS (STABLE + CLEAN)
# =====================================================
st.markdown("""
<style>

/* APP BACKGROUND */
.stApp {
    background-color: #ffffff;
}

/* ---------------- SIDEBAR (PowerBI style) ---------------- */
section[data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #fdeaea, #ffffff);
    border-right: 4px solid #c8102e;
}

section[data-testid="stSidebar"] h2 {
    color: #000000;
}

/* Filter cards */
.filter-card {
    background: white;
    padding: 12px;
    border-radius: 14px;
    margin-bottom: 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

/* Multiselect chips */
span[data-baseweb="tag"] {
    background-color: #c8102e !important;
    color: white !important;
}

/* ---------------- STICKY HEADER ---------------- */
.sticky-header {
    position: sticky;
    top: 0;
    z-index: 999;
    background: #00732f;
    padding: 26px 40px;
    margin-bottom: 30px;
    width: 100%;
    box-sizing: border-box;
}

/* ---------------- KPI CARDS ---------------- */
.kpi {
    background: #00732f;
    padding: 22px;
    border-radius: 18px;
    color: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
}
.kpi-title {
    font-size: 14px;
    opacity: 0.85;
}
.kpi-value {
    font-size: 32px;
    font-weight: 700;
}
.kpi-delta {
    font-size: 14px;
    opacity: 0.9;
}

/* ---------------- FOOTER ---------------- */
.footer {
    background: black;
    color: white;
    text-align: center;
    padding: 14px;
    margin-top: 60px;
    border-radius: 14px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HELPERS
# =====================================================
def fmt(n):
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f} B"
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f} M"
    return f"{n:,.0f}"

def yoy(curr, prev):
    if prev == 0:
        return "N/A"
    return f"{((curr - prev) / prev) * 100:.1f}%"

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("DLD_SAMPLE.csv")
    df["instance_date"] = pd.to_datetime(df["instance_date"], errors="coerce")
    df = df.dropna(subset=["instance_date", "Amount"])
    df["Year"] = df["instance_date"].dt.year
    df["Month"] = df["instance_date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.markdown("## 🔎 Filters")

years = sorted(df["Year"].unique())
areas = sorted(df["area_name_en"].dropna().unique())
types = sorted(df["property_type_en"].dropna().unique())

with st.sidebar.container():
    st.markdown('<div class="filter-card">📅 <b>Select Year</b>', unsafe_allow_html=True)
    sel_year = st.multiselect("", years, default=years[-3:])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="filter-card">📍 <b>Select Area</b>', unsafe_allow_html=True)
    sel_area = st.multiselect("", areas)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="filter-card">🏠 <b>Property Type</b>', unsafe_allow_html=True)
    sel_type = st.multiselect("", types)
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# APPLY FILTERS
# =====================================================
if sel_year:
    df = df[df["Year"].isin(sel_year)]
if sel_area:
    df = df[df["area_name_en"].isin(sel_area)]
if sel_type:
    df = df[df["property_type_en"].isin(sel_type)]

# =====================================================
# HEADER (STICKY + FIXED)
# =====================================================
st.markdown("""
<div class="sticky-header">
  <div style="
      display:flex;
      justify-content:space-between;
      align-items:center;
      max-width:1400px;
      margin:auto;
  ">
    <div>
      <h1 style="color:white; margin:0; font-size:34px;">
        AE UAE Real Estate Transactions Dashboard
      </h1>
      <p style="color:#e5e7eb; margin-top:6px;">
        Business Project – Interactive BI Dashboard
      </p>
    </div>
    <img src="assets/uae_flag.png" width="70">
  </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI + YoY
# =====================================================
current_year = df["Year"].max()
prev_year = current_year - 1

curr = df[df["Year"] == current_year]
prev = df[df["Year"] == prev_year]

c1, c2, c3 = st.columns(3)

c1.markdown(f"""
<div class="kpi">
<div class="kpi-title">Total Transactions</div>
<div class="kpi-value">{fmt(len(curr))}</div>
<div class="kpi-delta">YoY: {yoy(len(curr), len(prev))}</div>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="kpi">
<div class="kpi-title">Total Value (AED)</div>
<div class="kpi-value">{fmt(curr["Amount"].sum())}</div>
<div class="kpi-delta">YoY: {yoy(curr["Amount"].sum(), prev["Amount"].sum())}</div>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="kpi">
<div class="kpi-title">Average Value (AED)</div>
<div class="kpi-value">{fmt(curr["Amount"].mean())}</div>
<div class="kpi-delta">YoY: {yoy(curr["Amount"].mean(), prev["Amount"].mean())}</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# CHARTS
# =====================================================
st.subheader("📈 Monthly Transaction Value (AED)")
monthly = df.groupby("Month", as_index=False)["Amount"].sum()
fig1 = px.line(
    monthly,
    x="Month",
    y="Amount",
    markers=True,
    hover_data={"Amount": ":,.0f"}
)
fig1.update_traces(line_color="#00732f")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🏙️ Top Areas by Transaction Value")
top_areas = df.groupby("area_name_en", as_index=False)["Amount"].sum().nlargest(10, "Amount")
fig2 = px.bar(
    top_areas,
    x="area_name_en",
    y="Amount",
    hover_data={"Amount": ":,.0f"},
    color_discrete_sequence=["#c8102e"]
)
st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# DOWNLOAD
# =====================================================
# =====================================================
# EXPORT DATA (FILTER-BASED)
# =====================================================
st.subheader("⬇️ Export Data")

# Build descriptive filename
parts = []

if sel_year:
    parts.append(f"{min(sel_year)}_{max(sel_year)}")
if sel_area:
    parts.append("areas")
if sel_type:
    parts.append("types")

suffix = "_".join(parts) if parts else "all_data"
file_name = f"uae_real_estate_{suffix}.csv"

st.download_button(
    label="📥 Download Filtered CSV",
    data=df.to_csv(index=False),
    file_name=file_name,
    mime="text/csv"
)



# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div class="footer">
© UAE Real Estate Analytics Dashboard • Academic Project
</div>
""", unsafe_allow_html=True)
