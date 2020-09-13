from django.core.management.base import BaseCommand
from django.utils import timezone

from golf import models


class Command(BaseCommand):
    help = 'Close booking'

    '''
    python manage.py closebooking
    '''

    def handle(self, *args, **options):
        models.GolfBookingOrder.objects \
            .filter(order_status__in=[models.GolfBookingOrder.ORDER_STATUS_CHOICES.open,
                                      models.GolfBookingOrder.ORDER_STATUS_CHOICES.offered],
                    round_date__lt=timezone.make_aware(timezone.localtime().today())) \
            .update(order_status=models.GolfBookingOrder.ORDER_STATUS_CHOICES.closed)

        self.stdout.write(self.style.SUCCESS('Close booking'))
