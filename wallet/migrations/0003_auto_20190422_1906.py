# Generated by Django 2.2 on 2019-04-22 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0002_auto_20190422_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='user',
            new_name='owner',
        ),
        migrations.AddField(
            model_name='category',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
