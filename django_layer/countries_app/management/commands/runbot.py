from aiogram import executor
from django.core.management.base import BaseCommand

from aiogram_layer.src.app import dp


class Command(BaseCommand):
    def handle(self, *args, **options):
        return executor.start_polling(dp, skip_updates=True)
