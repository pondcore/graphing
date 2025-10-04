import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# โหลดข้อมูล
data1 = pd.read_csv("data1.csv")

# แปลงเวลาเป็น datetime
data1['Start Time'] = pd.to_datetime(data1['Start Time'], errors='coerce')

# -----------------------
# 📊 วาดกราฟเส้น Data1
fig, ax = plt.subplots(figsize=(12,6))

ax.plot(data1['Start Time'], data1['Volume'], marker='o', color='blue', label="Data1 Volume")

# ✅ format แกนเวลา
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
fig.autofmt_xdate()

ax.set_xlabel("Start Time")
ax.set_ylabel("Volume")
ax.set_title("Line Chart of Data1 (Start Time vs Volume)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)

# -----------------------
# ✅ เพิ่มตารางใต้กราฟ
table_data = data1[['Start Time','Volume']]
table_data['Start Time'] = table_data['Start Time'].dt.strftime("%Y-%m-%d %H:%M:%S")

table = plt.table(cellText=table_data.values,
                  colLabels=table_data.columns,
                  loc='bottom',
                  cellLoc='center',
                  bbox=[0.0, -0.5, 1.0, 0.4])  # [x, y, width, height]

plt.subplots_adjust(left=0.1, bottom=0.3)  # เว้นพื้นที่ให้ตาราง
plt.show()

# -----------------------
# ✅ export ข้อมูล
data1.to_csv("data1_with_table.csv", index=False)
print("✅ export เรียบร้อย: data1_with_table.csv")
