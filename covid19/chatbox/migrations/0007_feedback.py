# Generated by Django 3.0.3 on 2020-05-16 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbox', '0006_raise_issue'),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Feedback', models.TextField()),
                ('Email', models.EmailField(max_length=254)),
            ],
        ),
    ]
