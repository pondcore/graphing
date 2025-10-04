import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# โหลดข้อมูล
data1 = pd.read_csv("data1.csv")
data2 = pd.read_csv("data2.csv")

# แปลงเวลาเป็น datetime
data1['Start Time'] = pd.to_datetime(data1['Start Time'], errors='coerce')
data2['Read Time'] = pd.to_datetime(data2['Read Time'], errors='coerce')

# ✅ ฟังก์ชันเลือก record ใกล้ 08:00 ของแต่ละวัน
def closest_to_time(df, time_col, value_col, target="08:00:00"):
    result = []
    for date, group in df.groupby(df[time_col].dt.date):
        target_time = pd.to_datetime(str(date) + " " + target)
        idx = (group[time_col] - target_time).abs().idxmin()
        result.append(group.loc[idx, [time_col, value_col]])
    return pd.DataFrame(result)

# เลือกข้อมูลที่ใกล้ 8 โมง
data1_closest = closest_to_time(data1, "Start Time", "Volume")
data2_closest = closest_to_time(data2, "Read Time", "Volume")

# สร้างคอลัมน์ Date สำหรับ merge
data1_closest['Date'] = data1_closest['Start Time'].dt.date
data2_closest['Date'] = data2_closest['Read Time'].dt.date

# รวมข้อมูล
merged = pd.merge(
    data1_closest[['Date','Start Time','Volume']], 
    data2_closest[['Date','Read Time','Volume']], 
    on="Date", suffixes=('_data1','_data2')
)

# คำนวณ error
merged["Error"] = (merged["Volume_data1"] - merged["Volume_data2"]).abs()

# ✅ แปลงเวลาให้เป็น string แสดงละเอียด
merged['Start Time'] = merged['Start Time'].dt.strftime("%Y-%m-%d %H:%M:%S")
merged['Read Time'] = merged['Read Time'].dt.strftime("%Y-%m-%d %H:%M:%S")

# -----------------------
# 📊 วาดกราฟ + ตาราง
fig, ax = plt.subplots(figsize=(12,6))

# plot data1 + error bar
ax.errorbar(pd.to_datetime(merged['Start Time']), merged['Volume_data1'], 
            yerr=merged['Error'], fmt='o-', capsize=5, label="Data1 (Start Time)", color="blue")

# plot data2
ax.plot(pd.to_datetime(merged['Read Time']), merged['Volume_data2'], 
        's--', label="Data2 (Read Time)", color="orange")

# เส้นแดง 8 โมงเช้า
for d in merged['Date']:
    target_time = pd.to_datetime(str(d) + " 08:00:00")
    ax.axvline(target_time, color='red', linestyle='--', alpha=0.7)

# ✅ format แกนเวลา
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
fig.autofmt_xdate()

ax.set_xlabel("Time")
ax.set_ylabel("Volume")
ax.set_title("Volume vs Time (Data1 vs Data2) with 8AM Line + Error Bars")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)

# ✅ เพิ่มตารางใต้กราฟ
table_data = merged[['Start Time','Read Time','Error']]
table = plt.table(cellText=table_data.values,
                  colLabels=table_data.columns,
                  loc='bottom',
                  cellLoc='center',
                  bbox=[0.0, -0.5, 1.0, 0.4])  # [x, y, width, height]

plt.subplots_adjust(left=0.1, bottom=0.3)  # เว้นพื้นที่ให้ตาราง

plt.show()

# -----------------------
# ✅ export ข้อมูลรวมแล้ว
merged.to_csv("merged_with_error.csv", index=False)
merged.to_excel("merged_with_error.xlsx", index=False)

print("✅ export เรียบร้อย: merged_with_error.csv และ merged_with_error.xlsx")
