from pathlib import Path

import linebot
from django.core.management.base import BaseCommand
from linebot import models

from golf import models as golf_models


class Command(BaseCommand):
    help = 'Create rich menu'

    def add_arguments(self, parser):
        parser.add_argument('club',
                            nargs=1,
                            type=str,
                            help='Golf course')

        parser.add_argument('rich_menu_image_path',
                            nargs=1,
                            type=str,
                            help='Rich menu image')

    def handle(self, *args, **options):
        club = golf_models.GolfClub.objects.get(slug=options['club'][0])

        liff_app_request = golf_models.Liff.objects.get(golf_club=club, app_name='request')

        line_bot_api = linebot.LineBotApi(club.line_bot_channel_access_token)

        # Delete all rich menus
        rich_menu_list = line_bot_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            print(rich_menu.rich_menu_id)
            line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

        # Create rich menu
        rich_menu_to_create = models.RichMenu(
            size=models.RichMenuSize(width=2500, height=1686),
            # 2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="rich_menu",
            chat_bar_text="Menu",
            areas=[
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=models.URIAction(label='New Booking',
                                            uri=f'https://liff.line.me/{liff_app_request.liff_id}')),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=0, width=834, height=843),
                    action=models.MessageAction(label='My Booking', text='booking'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=0, width=833, height=843),
                    action=models.MessageAction(label='My settings', text='settings'), ),  # LIFF
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=843, width=833, height=843),
                    action=models.MessageAction(label='Promotions', text='promotions'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=843, width=834, height=843),
                    action=models.MessageAction(label='Price List', text='price'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=843, width=833, height=843),
                    action=models.MessageAction(label='Course Info', text='info'), ),
            ]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print("rich_menu_id", rich_menu_id)

        # Upload image and attach it to rich menu
        with open(Path(options['rich_menu_image_path'][0]), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

        # Set rich menu to default
        line_bot_api.set_default_rich_menu(rich_menu_id)

        self.stdout.write(self.style.SUCCESS('Made rich menu'))
