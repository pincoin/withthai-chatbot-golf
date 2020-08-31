def validate_round_date():
    return True


def validate_round_time():
    return True


def validate_pax(pax, **kwargs):
    golf_club = kwargs['golf_club']

    if golf_club.min_pax <= pax <= golf_club.max_pax:
        return True

    return False


def validate_cart():
    return True


def validate_customer_name():
    return True
