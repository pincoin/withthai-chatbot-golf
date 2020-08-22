from django import template

register = template.Library()


@register.simple_tag
def green_fee(green_fees, season, timeslot, customer_group):
    return f'{green_fees[season][timeslot][customer_group]:,.0f}'
