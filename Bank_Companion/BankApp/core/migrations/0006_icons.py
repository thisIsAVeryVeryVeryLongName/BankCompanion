# Generated by Django 2.0.7 on 2018-09-21 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180921_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Icons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('icon', models.CharField(max_length=255)),
            ],
        ),
    ]