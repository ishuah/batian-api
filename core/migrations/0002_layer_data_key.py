# Generated by Django 3.2.12 on 2022-03-25 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='data_key',
            field=models.CharField(default='pop_max', max_length=20),
            preserve_default=False,
        ),
    ]