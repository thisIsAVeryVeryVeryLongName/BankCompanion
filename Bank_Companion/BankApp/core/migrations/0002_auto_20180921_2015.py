# Generated by Django 2.0.7 on 2018-09-21 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='virtualbankaccount',
            old_name='transaction_tag_name',
            new_name='name',
        ),
    ]
