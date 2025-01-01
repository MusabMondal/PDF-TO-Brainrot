from django.core.management.base import BaseCommand

import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print(os.path.exists('C:\\Users\\musab\\OneDrive\\Documents\\Projects\\brainrot_learning\\brainrotlearning\\src\\media\\videos\\Minecraft_Parkour_gameplay_tiktok_format_9_16.mp4'))
