# Graph CPF 📊

A small Python project for data processing and visualization of CSV files (used in CPF graphing tasks).

## 🚀 Features
- Load and clean CSV data (`data1.csv`, `data2.csv`, etc.)
- Merge and resample data (30 min intervals, 08:00 closest records)
- Generate error reports and summary tables
- Simple plotting scripts (`join.py`, `data1.py`, `data2.py`)

## 🛠 Installation

Clone this repository:
```bash
git clone https://github.com/pondcore/graphing.git
cd graphing
```

Create and activate a virtual environment:
```bash
python -m venv venv
# Windows (PowerShell)
venv\Scripts\activate
# Git Bash / Linux / macOS
source venv/Scripts/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the main script:
```bash
python join.py
```

Other scripts:
```bash
join.py – merges datasets
data1.py, data2.py – preprocessing logic
```

📂 Project Structure
```lua
graphing/
│
├── app.py
├── main.py
├── join.py
├── show-error.py
├── data1.py
├── data2.py
├── requirements.txt
│
├── data1.csv
├── data2.csv
├── output.csv
├── merged_with_error.xlsx
└── ...
```
