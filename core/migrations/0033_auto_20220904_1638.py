# Generated by Django 3.0.3 on 2022-09-04 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20220904_1533'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Report',
            new_name='NewsItem',
        ),
    ]
