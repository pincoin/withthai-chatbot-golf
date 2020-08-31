from golf import models as golf_models


def is_holiday(round_date):
    if round_date.weekday() not in [5, 6]:
        return False

    try:
        golf_models.Holiday.objects.get(holiday=round_date)
    except golf_models.Holiday.DoesNotExist:
        return False

    return True


def calculate_green_fee():
    return 0
