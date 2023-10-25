import csv
import os

# 获取当前文件的路径
DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# 将文件名和路径组合，确保 DATA_FILE 和 dio.py 在同一个文件夹下
DATA_FILE = os.path.join(DIR_PATH, "when_data.csv")


def ensure_file_exists():
    try:
        with open(DATA_FILE, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["start_date", "duration"])
    except FileExistsError:
        pass


def load_periods():
    records = []
    ensure_file_exists()
    with open(DATA_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            records.append({"start_date": row[0], "duration": row[1]})
    return records


def save_period(start_date, duration):
    ensure_file_exists()
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([start_date, duration])
