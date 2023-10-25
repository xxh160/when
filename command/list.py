from datetime import datetime, timedelta
from data.dio import load_periods


def execute(num_records):
    origin_records = load_periods()
    records = sorted(
        origin_records, key=lambda x: datetime.strptime(x["start_date"], "%Y.%m.%d")
    )

    if num_records != -1:
        records = records[-num_records:]

    for record in records:
        start_date = datetime.strptime(record["start_date"], "%Y.%m.%d")
        end_date = start_date + timedelta(days=int(record["duration"]))

        # 使用strftime进行格式化
        formatted_start_date = start_date.strftime("%Y.%m.%d")
        formatted_end_date = end_date.strftime("%Y.%m.%d")

        print(f"Start date: {formatted_start_date}, End date: {formatted_end_date}")
