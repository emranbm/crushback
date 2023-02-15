# Generated by Django 4.1.6 on 2023-02-15 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_chat_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram_username',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
    ]
