import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
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

# Correct order for hours
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

# Title
st.title("💧 Hostel Water Consumption Dashboard")

st.markdown("Real-time style analysis of hourly hostel water usage patterns.")

# KPI Cards
total_usage = round(df["Water_Usage"].sum(), 2)
average_usage = round(df["Water_Usage"].mean(), 2)
average_leakage = round(df["Leakage_Percentage"].mean(), 2)
total_students = df["Students"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Water Usage", f"{total_usage} L")
col2.metric("Average Usage", f"{average_usage} L")
col3.metric("Average Leakage", f"{average_leakage}%")
col4.metric("Total Students", total_students)

st.divider()

# Hourly usage trend
hourly_usage = df.groupby("Hour_Label")["Water_Usage"].mean().reset_index()

fig1 = px.line(
    hourly_usage,
    x="Hour_Label",
    y="Water_Usage",
    markers=True,
    title="Average Hourly Water Usage"
)

st.plotly_chart(fig1, use_container_width=True)

# Block-wise comparison
block_usage = df.groupby("Hostel_Block")["Water_Usage"].sum().reset_index()

fig2 = px.bar(
    block_usage,
    x="Hostel_Block",
    y="Water_Usage",
    color="Hostel_Block",
    title="Total Water Usage by Hostel Block"
)

st.plotly_chart(fig2, use_container_width=True)

# Leakage vs usage
fig3 = px.scatter(
    df,
    x="Leakage_Percentage",
    y="Water_Usage",
    color="Hostel_Block",
    hover_data=["Students"],
    title="Leakage Percentage vs Water Usage"
)

st.plotly_chart(fig3, use_container_width=True)

# Heatmap
heatmap_data = df.pivot_table(
    values="Water_Usage",
    index="Hostel_Block",
    columns="Hour_Label",
    aggfunc="mean"
)

fig4 = px.imshow(
    heatmap_data,
    aspect="auto",
    title="Hourly Water Usage Heatmap"
)

st.plotly_chart(fig4, use_container_width=True)

# Top consuming blocks
top_blocks = (
    df.groupby("Hostel_Block")["Water_Usage"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig5 = px.pie(
    top_blocks,
    names="Hostel_Block",
    values="Water_Usage",
    title="Water Consumption Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# Raw dataset
st.subheader("Dataset Preview")

st.dataframe(df.head(50), use_container_width=True)