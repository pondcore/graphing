import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# 1. โหลดข้อมูล
# -------------------------
data1 = pd.read_csv("./data1.csv")
data2 = pd.read_csv("./data2.csv")

# -------------------------
# 2. แปลงเวลาเป็น datetime
# -------------------------
data1['Start Time'] = pd.to_datetime(data1['Start Time'])
data1['Stop Time'] = pd.to_datetime(data1['Stop Time'])
data2['Read Time'] = pd.to_datetime(data2['Read Time'])

# -------------------------
# 3. ดึงข้อมูลที่ใกล้ 08:00 ของแต่ละวัน
# -------------------------
target_time = "08:00:00"

# ฟังก์ชันหาค่าใกล้เวลาเป้าหมาย
def get_closest(df, time_col, group_col='date'):
    df[group_col] = df[time_col].dt.date
    target = pd.to_datetime(df[group_col].astype(str) + " " + target_time)
    idx = (df[time_col] - target).abs().groupby(df[group_col]).idxmin()
    return df.loc[idx]

closest1 = get_closest(data1, "Start Time")
closest2 = get_closest(data2, "Read Time")

# -------------------------
# 4. รวมข้อมูลตามวันที่
# -------------------------
merged = pd.merge(
    closest1[['Start Time', 'Volume', 'date']],
    closest2[['Read Time', 'Volume', 'date']],
    on="date",
    suffixes=('_data1', '_data2')
)

# คำนวณ error (ส่วนต่าง)
merged['Error'] = (merged['Volume_data1'] - merged['Volume_data2']).abs()

print(merged.head())

# -------------------------
# 5. วาดกราฟ
# -------------------------
plt.figure(figsize=(10,6))

plt.plot(merged['date'], merged['Volume_data1'], 'o-', label="Data1 (Start Time)")
plt.plot(merged['date'], merged['Volume_data2'], 's-', label="Data2 (Read Time)")

# error bar
plt.errorbar(
    merged['date'],
    merged['Volume_data1'],
    yerr=merged['Error'],
    fmt='o',
    ecolor='red',
    capsize=5,
    label="Error"
)

plt.xlabel("Date")
plt.ylabel("Volume")
plt.title("Volume Comparison near 08:00")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
