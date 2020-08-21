from django import template

register = template.Library()


@register.simple_tag
def green_fee(rates, season, timeslot, customer_group):
    return f'{rates[season][timeslot][customer_group]:,.0f}'
