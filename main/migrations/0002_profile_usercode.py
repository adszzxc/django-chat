# Generated by Django 2.0.7 on 2018-07-07 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='usercode',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]