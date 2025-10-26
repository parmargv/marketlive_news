from datetime import date

# List of holidays in 2024 (corrected with commas)
holidays = [
    "2024-01-22",  # New Year's Day
    "2024-01-26",  # Martin Luther King Jr. Day
    "2024-03-08",  # Presidents' Day
    "2024-03-25",  # Memorial Day
    "2024-03-29",  # Independence Day
    "2024-04-11",  # Labor Day
    "2024-05-01",  # Columbus Day
    "2024-05-20",  # Veterans Day
    "2024-06-17",  # Thanksgiving Day
    "2024-07-17",  # Christmas Day
    "2024-08-15",  # Christmas Day
    "2024-10-02",  # Christmas Day
    "2024-11-01",  # Christmas Day
    "2024-11-15",  # Christmas Day
    "2024-12-25"   # Christmas Day
]

def is_holiday(check_date):
    return check_date.strftime("%Y-%m-%d") in holidays

def is_working_day(check_date):
    # Check if the day is Saturday (5) or Sunday (6)
    if check_date.weekday() >= 5:
        return False
    # Check if the day is a holiday
    if is_holiday(check_date):
        return False
    return True

# Example usage:
# today = date.today()
# print(is_working_day(today))