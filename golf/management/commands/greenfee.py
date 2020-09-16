import json
from pathlib import Path

from django.core.management.base import BaseCommand

from golf import models


class Command(BaseCommand):
    help = 'Create price table'

    '''
    python manage.py greenfee with-thai /home/ubuntu/Projects/withthai/golf/static/golf/json/green_fee.json
    
    green_fee.json format
    Array: Seasons x Timeslots x Customer groups
    
    [
        [
            [0, 600, 2500, 3500],
            [500, 800, 1800, 2000],
            [900, 900, 1600, 1600],
            [0, 800, 3000, 4500],
            [0, 800, 3000, 4500],
            [500, 800, 1800, 2000],
            [900, 900, 1600, 1600]
        ]
    ]
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
        green_fee_dict = json.loads(open(Path(options['price_table_json_path'][0])).read())

        seasons = models.Season.objects \
            .filter(golf_club__slug=options['club'][0]) \
            .order_by('season_start')

        timeslots = models.Timeslot.objects \
            .filter(golf_club__slug=options['club'][0]) \
            .order_by('day_of_week', 'slot_start')

        customer_groups = models.CustomerGroup.objects \
            .filter(golf_club__slug=options['club'][0]).order_by('position')

        models.GreenFee.objects \
            .filter(season__golf_club__slug=options['club'][0],
                    timeslot__golf_club__slug=options['club'][0],
                    customer_group__golf_club__slug=options['club'][0]) \
            .delete()

        for i, season in enumerate(seasons):
            for j, timeslot in enumerate(timeslots):
                for k, customer_group in enumerate(customer_groups):
                    green_fee = models.GreenFee()
                    green_fee.season = season
                    green_fee.timeslot = timeslot
                    green_fee.customer_group = customer_group
                    green_fee.list_price = green_fee.selling_price = green_fee_dict[i][j][k]
                    green_fee.save()

        self.stdout.write(self.style.SUCCESS('Created green fee table'))
