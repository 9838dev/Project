# Generated by Django 3.0.3 on 2020-05-15 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbox', '0004_delete_trade_feed'),
    ]

    operations = [
        migrations.CreateModel(
            name='trade_feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254)),
                ('Trade', models.TextField()),
            ],
        ),
    ]
