import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Hostel Water Consumption Dashboard",
    layout="wide"
)

# Load dataset
df = pd.read_csv("hostel_hourly_water_usage.csv")

# Convert hour into AM/PM labels
df["Hour_Label"] = df["Hour"].apply(
    lambda x: f"{x % 12 if x % 12 != 0 else 12} {'AM' if x < 12 else 'PM'}"
)

# Correct hour order
hour_order = [
    "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM",
    "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
    "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM",
    "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"
]

df["Hour_Label"] = pd.Categorical(
    df["Hour_Label"],
    categories=hour_order,
    ordered=True
)

# Correct hostel block order
block_order = [f"Block_{i}" for i in range(1, 16)]

df["Hostel_Block"] = pd.Categorical(
    df["Hostel_Block"],
    categories=block_order,
    ordered=True
)

# Dashboard title
st.title("💧 Hostel Water Consumption Dashboard")

st.markdown(
    "Interactive analysis of hourly water consumption patterns across hostel blocks."
)

# =========================
# KPI Metrics
# =========================

# Average daily usage instead of huge cumulative value
daily_usage = (
    df.groupby("Date")["Water_Usage"]
    .sum()
    .mean()
)

average_daily_usage = round(daily_usage, 2)

# Average usage
avg_usage = round(df["Water_Usage"].mean(), 2)

# Average leakage
avg_leakage = round(df["Leakage_Percentage"].mean(), 2)

# Count students only once per block
total_students = (
    df.groupby("Hostel_Block")["Students"]
    .first()
    .sum()
)

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Daily Usage", f"{average_daily_usage} L")
col2.metric("Average Hourly Usage", f"{avg_usage} L")
col3.metric("Average Leakage", f"{avg_leakage}%")
col4.metric("Total Students", total_students)

st.divider()

# =========================
# Hourly Water Usage Trend
# =========================

hourly_usage = (
    df.groupby("Hour_Label")["Water_Usage"]
    .mean()
    .reset_index()
)

fig1 = px.line(
    hourly_usage,
    x="Hour_Label",
    y="Water_Usage",
    markers=True,
    title="Average Hourly Water Usage",
    category_orders={"Hour_Label": hour_order}
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# Total Usage by Hostel Block
# =========================

block_usage = (
    df.groupby("Hostel_Block")["Water_Usage"]
    .sum()
    .reset_index()
)

block_usage["Block_Number"] = (
    block_usage["Hostel_Block"]
    .astype(str)
    .str.extract(r'(\d+)')
    .astype(int)
)

block_usage = block_usage.sort_values("Block_Number")

fig2 = px.bar(
    block_usage,
    x="Hostel_Block",
    y="Water_Usage",
    color="Hostel_Block",
    title="Total Water Usage by Hostel Block",
    category_orders={"Hostel_Block": block_order}
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# Leakage vs Usage
# =========================

fig3 = px.scatter(
    df,
    x="Leakage_Percentage",
    y="Water_Usage",
    color="Hostel_Block",
    hover_data=["Students"],
    title="Leakage Percentage vs Water Usage",
    category_orders={"Hostel_Block": block_order}
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# Heatmap
# =========================

heatmap_data = df.pivot_table(
    values="Water_Usage",
    index="Hostel_Block",
    columns="Hour_Label",
    aggfunc="mean"
)

heatmap_data = heatmap_data.reindex(block_order)

fig4 = px.imshow(
    heatmap_data,
    aspect="auto",
    title="Hourly Water Usage Heatmap"
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# Pie Chart
# =========================

pie_data = (
    df.groupby("Hostel_Block")["Water_Usage"]
    .sum()
    .reset_index()
)

pie_data["Block_Number"] = (
    pie_data["Hostel_Block"]
    .astype(str)
    .str.extract(r'(\d+)')
    .astype(int)
)

pie_data = pie_data.sort_values("Block_Number")

fig5 = px.pie(
    pie_data,
    names="Hostel_Block",
    values="Water_Usage",
    title="Water Consumption Distribution",
    category_orders={"Hostel_Block": block_order}
)

st.plotly_chart(fig5, use_container_width=True)

# =========================
# Dataset Preview
# =========================

st.subheader("Dataset Preview")

st.dataframe(df.head(50), use_container_width=True)