from datetime import datetime, timedelta
from data.dio import load_periods

DEFAULT_ALPHA = 0.3


def split_into_continuous_groups(sorted_dates):
    """根据日期分割为连续的组, 每个组的日期是连续的"""
    groups = []
    current_group = [sorted_dates[0]]

    for i in range(1, len(sorted_dates)):
        prev_date = datetime.strptime(current_group[-1]["start_date"], "%Y.%m.%d")
        curr_date = datetime.strptime(sorted_dates[i]["start_date"], "%Y.%m.%d")
        if (curr_date - prev_date).days > 45:  # 超过 45 天认为是断裂的
            groups.append(current_group)
            current_group = []
        current_group.append(sorted_dates[i])

    if current_group:
        groups.append(current_group)

    # 过滤掉长度小于2的组
    groups = [group for group in groups if len(group) >= 2]

    return groups


def calculate_grouped_avg_cycle(group):
    """计算给定日期组的平均周期"""
    intervals = []
    for i in range(1, len(group)):
        start_date_previous = datetime.strptime(group[i - 1]["start_date"], "%Y.%m.%d")
        start_date_current = datetime.strptime(group[i]["start_date"], "%Y.%m.%d")
        interval = (start_date_current - start_date_previous).days
        intervals.append(interval)

    return sum(intervals) / len(intervals)


def calculate_final_avg_cycle(dates):
    sorted_dates = sorted(
        dates, key=lambda x: datetime.strptime(x["start_date"], "%Y.%m.%d")
    )
    continuous_groups = split_into_continuous_groups(sorted_dates)

    avg_intervals = [calculate_grouped_avg_cycle(group) for group in continuous_groups]

    # 返回默认周期: 31 天
    if len(avg_intervals) == 0:
        return 31

    # 加权平均所有的平均值
    weighted_avg = avg_intervals[0]
    for avg in avg_intervals[1:]:
        weighted_avg = DEFAULT_ALPHA * avg + (1 - DEFAULT_ALPHA) * weighted_avg

    return weighted_avg


def predict_next_period(dates, given_date):
    final_avg_cycle = calculate_final_avg_cycle(dates)
    sorted_dates = sorted(
        dates, key=lambda x: datetime.strptime(x["start_date"], "%Y.%m.%d")
    )

    # 找到小于 given_date 但是最大的日期
    last_period_start = None
    for record in reversed(sorted_dates):
        date = datetime.strptime(record["start_date"], "%Y.%m.%d")
        if date < given_date:
            last_period_start = date
            break

    if last_period_start is None:
        raise ValueError("There's no date less than the given_date in the records.")

    next_period_start = last_period_start

    # 找到下一个大于给定日期的月经开始日期
    while next_period_start <= given_date:
        next_period_start += timedelta(days=final_avg_cycle)

    return next_period_start, next_period_start + timedelta(
        days=predict_duration(dates)
    ), final_avg_cycle


def predict_duration(dates):
    durations = [int(date["duration"]) for date in dates]
    return sum(durations) / len(durations)


def execute(given_date):
    given_date = datetime.strptime(given_date, "%Y.%m.%d")
    dates = load_periods()
    start, end, cycle= predict_next_period(dates, given_date)

    print(f"Predicted menstrual cycle duration: {cycle:.2f} days")
    print(
        f"Next predicted menstrual cycle: {start.strftime('%Y.%m.%d')} to {end.strftime('%Y.%m.%d')}"
    )
