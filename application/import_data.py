import os
import pandas as pd
from django.core.wsgi import get_wsgi_application

# Charger les paramètres Django pour que le script puisse accéder à la configuration de l'application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votre_projet.settings')
application = get_wsgi_application()

from application.models import Country, Title, WeeklyRanking

csv_path = './data/all-weeks-countries.csv'

df = pd.read_csv(csv_path)

# Création des objets Country et Title
countries = {iso2: Country.objects.get_or_create(iso2=iso2, name=name)[0] for iso2, name in zip(df['country_iso2'], df['country_name'])}
titles = {title: Title.objects.get_or_create(show_title=title, season_title=season)[0] for title, season in zip(df['show_title'], df['season_title'])}

# Importation des classements hebdomadaires
for index, row in df.iterrows():
    WeeklyRanking.objects.create(
        country=countries[row['country_iso2']],
        week=row['week'],
        category=row['category'],
        title=titles[row['show_title']],
        weekly_rank=row['weekly_rank'],
        cumulative_weeks_in_top_10=row['cumulative_weeks_in_top_10']
    )
