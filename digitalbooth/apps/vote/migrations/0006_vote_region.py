# Generated by Django 3.0.8 on 2020-08-24 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_auto_20200824_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='region',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
