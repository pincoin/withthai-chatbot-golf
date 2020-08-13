import linebot
from django.core.management.base import BaseCommand

from golf.models import GolfClub


class Command(BaseCommand):
    help = 'Delete rich menu'

    def add_arguments(self, parser):
        parser.add_argument('club',
                            nargs=1,
                            type=str,
                            help='Golf course')

    def handle(self, *args, **options):
        club = GolfClub.objects.get(slug=options['club'][0])

        line_bot_api = linebot.LineBotApi(club.line_bot_channel_access_token)

        rich_menu_list = line_bot_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            print(rich_menu.rich_menu_id)
            line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

        self.stdout.write(self.style.SUCCESS('Deleted rich menu'))
