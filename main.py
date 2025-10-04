import pandas as pd

# อ่านจากไฟล์
df = pd.read_csv("./data.txt", sep="/")

# ทำความสะอาด " และ \N
df = df.replace({'"': '', '\\N': None})

# แสดงผลลัพธ์
print(df)

# หรือบันทึกเป็น CSV
df.to_csv("output.csv", index=False)
