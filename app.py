import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Data1 vs Data2 Dashboard", layout="wide")
st.title("📊 Data1 vs Data2 Comparison Dashboard")

# --------------------------
# โหลดข้อมูล
# --------------------------
data1 = pd.read_csv("data1.csv")
data2 = pd.read_csv("data2.csv")

# แปลงเวลาเป็น datetime
data1['Start Time'] = pd.to_datetime(data1['Start Time'], errors='coerce')
data2['Read Time'] = pd.to_datetime(data2['Read Time'], errors='coerce')

# สร้างคอลัมน์ Date
data1['Date'] = data1['Start Time'].dt.date
data2['Date'] = data2['Read Time'].dt.date

# รวมข้อมูลตามวันที่
merged = pd.merge(
    data1[['Date', 'Start Time', 'Volume']],
    data2[['Date', 'Read Time', 'Volume']],
    on="Date",
    suffixes=('_data1', '_data2')
)

# คำนวณ Error Absolute
merged['Error'] = (merged['Volume_data1'] - merged['Volume_data2']).abs()

# --------------------------
# วาดกราฟ
# --------------------------
fig = go.Figure()

# Data1 + Error Bar
fig.add_trace(go.Scatter(
    x=merged['Start Time'],
    y=merged['Volume_data1'],
    error_y=dict(type='data', array=merged['Error'], visible=True),
    mode='lines+markers',
    name='Data1',
    line=dict(color='blue')
))

# Data2
fig.add_trace(go.Scatter(
    x=merged['Read Time'],
    y=merged['Volume_data2'],
    mode='lines+markers',
    name='Data2',
    line=dict(color='orange', dash='dash')
))

# เส้นแดงแนวตั้งเวลา 08:00 ของแต่ละวัน
for d in merged['Date'].unique():
    ts = pd.to_datetime(str(d)) + pd.Timedelta(hours=8)  # ✅ fix เป็น Timestamp เดี่ยว
    fig.add_vline(
        x=ts,
        line=dict(color="red", dash="dot"),
        annotation_text="08:00",
        annotation_position="top left"
    )

# Layout
fig.update_layout(
    title="📊 Data1 vs Data2 with 8AM Line and Error Bars",
    xaxis_title="Time",
    yaxis_title="Volume",
    legend=dict(x=0, y=1),
    template="plotly_white",
    height=600
)

# แสดงผลใน Streamlit
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# ตารางข้อมูล
# --------------------------
st.subheader("📑 Merged Data with Error")
st.dataframe(merged)
