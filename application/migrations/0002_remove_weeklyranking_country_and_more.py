# Generated by Django 5.0 on 2024-01-05 05:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="weeklyranking",
            name="country",
        ),
        migrations.RemoveField(
            model_name="weeklyranking",
            name="title",
        ),
        migrations.DeleteModel(
            name="Country",
        ),
        migrations.DeleteModel(
            name="Title",
        ),
        migrations.DeleteModel(
            name="WeeklyRanking",
        ),
    ]
