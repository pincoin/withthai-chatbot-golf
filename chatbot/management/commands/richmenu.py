from pathlib import Path

import linebot
from django.core.management.base import BaseCommand
from linebot import models

from golf import models as golf_models


class Command(BaseCommand):
    help = 'Create rich menu'

    '''
    python manage.py richmenu with-thai /home/ubuntu/Projects/withthai/liff/static/images/liff/with_thai_rich_menu.jpg
    '''

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

        line_rich_menu = {}

        line_bot_api = linebot.LineBotApi(club.line_bot_channel_access_token)

        # Delete all rich menus
        rich_menu_list = line_bot_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            print(rich_menu.rich_menu_id)
            line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

        # Create rich menu (English-default)
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=models.RichMenu(
            size=models.RichMenuSize(width=2500, height=1686),
            # 2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="rich_menu",
            chat_bar_text="Menu",
            areas=[
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=models.MessageAction(label='My Booking', text='Booking'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=0, width=834, height=843),
                    action=models.URIAction(label='Price Table',
                                            uri=f"https://liff.line.me/{club.liff['price']['en']['id']}"), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=0, width=833, height=843),
                    action=models.MessageAction(label='Course', text='Course'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=843, width=833, height=843),
                    action=models.MessageAction(label='Promotions', text='Promotions'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=843, width=834, height=843),
                    action=models.MessageAction(label='Hot Deals', text='Deals'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=843, width=833, height=843),
                    action=models.MessageAction(label='Coupons', text='Coupons'), ),
            ]
        ))
        line_rich_menu['default'] = rich_menu_id
        line_rich_menu['en'] = rich_menu_id
        print("rich_menu_id", rich_menu_id)

        # Upload image and attach it to rich menu
        with open(Path(options['rich_menu_image_path'][0]), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

        # Set rich menu to default
        line_bot_api.set_default_rich_menu(rich_menu_id)

        # Create rich menu (Korean)
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=models.RichMenu(
            size=models.RichMenuSize(width=2500, height=1686),
            # 2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="rich_menu",
            chat_bar_text="Menu",
            areas=[
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=models.MessageAction(label='나의 예약', text='Booking'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=0, width=834, height=843),
                    action=models.URIAction(label='요금표',
                                            uri=f"https://liff.line.me/{club.liff['price']['ko']['id']}"), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=0, width=833, height=843),
                    action=models.MessageAction(label='골프장', text='Course'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=843, width=833, height=843),
                    action=models.MessageAction(label='프로모션', text='Promotions'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=843, width=834, height=843),
                    action=models.MessageAction(label='핫딜', text='Deals'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=843, width=833, height=843),
                    action=models.MessageAction(label='쿠폰', text='Coupons'), ),
            ]
        ))
        line_rich_menu['ko'] = rich_menu_id
        print("rich_menu_id", rich_menu_id)

        # Upload image and attach it to rich menu
        with open(Path(options['rich_menu_image_path'][0]), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

        # Create rich menu (Thai)
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=models.RichMenu(
            size=models.RichMenuSize(width=2500, height=1686),
            # 2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="rich_menu",
            chat_bar_text="Menu",
            areas=[
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=models.MessageAction(label='My Booking', text='Booking'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=0, width=834, height=843),
                    action=models.URIAction(label='Price Table',
                                            uri=f"https://liff.line.me/{club.liff['price']['th']['id']}"), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=0, width=833, height=843),
                    action=models.MessageAction(label='Course', text='Course'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=843, width=833, height=843),
                    action=models.MessageAction(label='Promotions', text='Promotions'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=843, width=834, height=843),
                    action=models.MessageAction(label='Hot Deals', text='Deals'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=843, width=833, height=843),
                    action=models.MessageAction(label='Coupons', text='Coupons'), ),
            ]
        ))
        line_rich_menu['th'] = rich_menu_id
        print("rich_menu_id", rich_menu_id)

        # Upload image and attach it to rich menu
        with open(Path(options['rich_menu_image_path'][0]), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

        '''
        # Create rich menu (Japanese)
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=models.RichMenu(
            size=models.RichMenuSize(width=2500, height=1686),
            # 2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="rich_menu",
            chat_bar_text="Menu",
            areas=[
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=models.MessageAction(label='My Booking', text='Booking'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=0, width=834, height=843),
                    action=models.URIAction(label='Price Table',
                                            uri=f"https://liff.line.me/{club.liff['price']['jp']['id']}"), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=0, width=833, height=843),
                    action=models.MessageAction(label='Course', text='Course'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=843, width=833, height=843),
                    action=models.MessageAction(label='Promotions', text='Promotions'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=843, width=834, height=843),
                    action=models.MessageAction(label='Hot Deals', text='Deals'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=843, width=833, height=843),
                    action=models.MessageAction(label='Coupons', text='Coupons'), ),
            ]
        ))
        line_rich_menu['jp'] = rich_menu_id
        print("rich_menu_id", rich_menu_id)

        # Upload image and attach it to rich menu
        with open(Path(options['rich_menu_image_path'][0]), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

        # Create rich menu (Chinese)
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=models.RichMenu(
            size=models.RichMenuSize(width=2500, height=1686),
            # 2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="rich_menu",
            chat_bar_text="Menu",
            areas=[
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=0, width=833, height=843),
                    action=models.MessageAction(label='My Booking', text='Booking'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=0, width=834, height=843),
                    action=models.URIAction(label='Price Table',
                                            uri=f"https://liff.line.me/{club.liff['price']['cn']['id']}"), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=0, width=833, height=843),
                    action=models.MessageAction(label='Course', text='Course'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=0, y=843, width=833, height=843),
                    action=models.MessageAction(label='Promotions', text='Promotions'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=833, y=843, width=834, height=843),
                    action=models.MessageAction(label='Hot Deals', text='Deals'), ),
                models.RichMenuArea(
                    bounds=models.RichMenuBounds(x=1667, y=843, width=833, height=843),
                    action=models.MessageAction(label='Coupons', text='Coupons'), ),
            ]
        ))
        line_rich_menu['cn'] = rich_menu_id
        print("rich_menu_id", rich_menu_id)

        # Upload image and attach it to rich menu
        with open(Path(options['rich_menu_image_path'][0]), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
        '''

        # Save rich menu json field
        club.line_rich_menu = line_rich_menu
        club.save()

        self.stdout.write(self.style.SUCCESS('Made rich menu'))
