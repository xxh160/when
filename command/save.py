from datetime import datetime
from data.dio import save_period

def execute(dates):
    start_date = dates[0]
    end_date = datetime.strptime(dates[1], "%Y.%m.%d")
    start_date_obj = datetime.strptime(start_date, "%Y.%m.%d")

    duration = (end_date - start_date_obj).days + 1

    save_period(start_date, duration)
    print("Data saved")
