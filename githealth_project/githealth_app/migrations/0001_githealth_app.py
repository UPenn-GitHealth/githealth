# Generated by Django 4.2.7 on 2023-11-25 21:02

from django.db import migrations
import random

def create_data(apps, schema_editor):
    IssueMetric = apps.get_model('githealth_app', 'IssueMetric')
    
    # Dummy data
    for year in [2021, 2022]:
        for month in range(1, 13):
            IssueMetric.objects.create(
                year=year,
                month=month,
                average_time_to_first_response=random.uniform(10, 40), 
                average_time_to_close=random.uniform(50, 120), 
                total_issues_opened=random.randint(100, 500), 
                total_issues_closed=random.randint(80, 450),
                contributor_count=random.randint(10, 100), 
            )

class Migration(migrations.Migration):
    dependencies = [
    ]
    operations = [
        migrations.RunPython(create_data),
    ]