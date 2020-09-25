from django.core.management.base import BaseCommand
from django.utils import timezone

from golf import models


class Command(BaseCommand):
    help = 'Delete booking'

    '''
    python manage.py deletebooking
    '''

    def handle(self, *args, **options):
        models.GolfBookingOrder.objects \
            .select_related('line_user') \
            .filter(payment_status=models.GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid,
                    line_user__follow_status=models.LineUser.FOLLOW_CHOICES.unfollow,
                    round_date__lt=timezone.make_aware(timezone.localtime().today())) \
            .exclude(order_status=models.GolfBookingOrder.ORDER_STATUS_CHOICES.confirmed) \
            .delete()

        self.stdout.write(self.style.SUCCESS('Delete booking'))
