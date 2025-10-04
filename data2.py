import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# โหลดข้อมูล
data2 = pd.read_csv("data2.csv")

# แปลงเวลาเป็น datetime
data2['Read Time'] = pd.to_datetime(data2['Read Time'], errors='coerce')

# -----------------------
# 📊 วาดกราฟเส้น Data2
fig, ax = plt.subplots(figsize=(12,6))

ax.plot(data2['Read Time'], data2['Volume'], marker='s', color='orange', label="Data2 Volume")

# ✅ format แกนเวลา
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
fig.autofmt_xdate()

ax.set_xlabel("Read Time")
ax.set_ylabel("Volume")
ax.set_title("Line Chart of Data2 (Read Time vs Volume)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)

# -----------------------
# ✅ เพิ่มตารางใต้กราฟ
table_data = data2[['Read Time','Volume']].copy()
table_data['Read Time'] = table_data['Read Time'].dt.strftime("%Y-%m-%d %H:%M:%S")

table = plt.table(cellText=table_data.values,
                  colLabels=table_data.columns,
                  loc='bottom',
                  cellLoc='center',
                  bbox=[0.0, -0.5, 1.0, 0.4])  # [x, y, width, height]

plt.subplots_adjust(left=0.1, bottom=0.3)  # เว้นพื้นที่ให้ตาราง
plt.show()

# -----------------------
# ✅ export ข้อมูล
data2.to_csv("data2_with_table.csv", index=False)
print("✅ export เรียบร้อย: data2_with_table.csv")
