# Generated by Django 4.1.6 on 2023-03-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_matchedrecord'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='crush',
            constraint=models.UniqueConstraint(fields=('telegram_username', 'crusher'), name='duplicate_crush_preventer'),
        ),
    ]
