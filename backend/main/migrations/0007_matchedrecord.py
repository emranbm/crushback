# Generated by Django 4.1.6 on 2023-02-24 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_make_telegram_info_optional'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchedRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matched_at', models.DateTimeField(auto_now_add=True)),
                ('informed', models.BooleanField(default=False)),
                ('left_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('right_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='matchedrecord',
            constraint=models.UniqueConstraint(fields=('left_user', 'right_user'), name='unique_matched_record_users'),
        ),
    ]
