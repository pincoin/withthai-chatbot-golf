import json
from pathlib import Path

from django.core.management.base import BaseCommand

from golf import models


class Command(BaseCommand):
    help = 'Create price table'

    '''
    python manage.py rate with-thai /home/ubuntu/Projects/withthai/golf/static/js/golf/json/rate.json
    '''

    def add_arguments(self, parser):
        parser.add_argument('club',
                            nargs=1,
                            type=str,
                            help='Golf course')

        parser.add_argument('price_table_json_path',
                            nargs=1,
                            type=str,
                            help='Price table json')

    def handle(self, *args, **options):
        rate_dict = json.loads(open(Path(options['price_table_json_path'][0])).read())

        seasons = models.Season.objects \
            .filter(golf_club__slug=options['club'][0]) \
            .order_by('season_start')

        timeslots = models.Timeslot.objects \
            .filter(golf_club__slug=options['club'][0]) \
            .order_by('day_of_week', 'slot_start')

        customer_groups = models.CustomerGroup.objects \
            .filter(golf_club__slug=options['club'][0]).order_by('position')

        models.Rate.objects \
            .filter(season__golf_club__slug=options['club'][0],
                    timeslot__golf_club__slug=options['club'][0],
                    customer_group__golf_club__slug=options['club'][0]) \
            .delete()

        for i, season in enumerate(seasons):
            for j, timeslot in enumerate(timeslots):
                for k, customer_group in enumerate(customer_groups):
                    rate = models.Rate()
                    rate.season = season
                    rate.timeslot = timeslot
                    rate.customer_group = customer_group
                    rate.green_fee_list_price = rate.green_fee_selling_price = rate_dict[i][j][k]
                    rate.save()

        self.stdout.write(self.style.SUCCESS('Created price table'))
