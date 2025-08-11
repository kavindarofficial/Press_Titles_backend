# api/management/commands/load_titles.py
import pandas as pd
from django.core.management.base import BaseCommand
from api.models import NewspaperTitle

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        newspapers_df = pd.read_csv(r'C:\stuff\Automated-Online-System-to-Verify-Duplicate-Press-Titles\backend\IndianNewsPaper.csv')
        for title in newspapers_df['Name'].dropna():
            NewspaperTitle.objects.get_or_create(name=title.lower())

        self.stdout.write(self.style.SUCCESS('Successfully loaded newspaper titles'))
