# Generated by Django 2.0.7 on 2018-09-22 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180922_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='virtual_bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.VirtualBankAccount'),
        ),
    ]
