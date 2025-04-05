# Generated by Django 4.2.11 on 2025-04-05 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('color', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
    ]
