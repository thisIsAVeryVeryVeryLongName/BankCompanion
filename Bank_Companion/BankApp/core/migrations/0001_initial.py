# Generated by Django 2.0.7 on 2018-09-21 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.IntegerField(default=0)),
                ('balance', models.FloatField(default=0.0)),
                ('iban', models.CharField(max_length=255)),
                ('bic', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_delete_user', 'Delete User'), ('can_create_user', 'Create User'), ('can_edit_user', 'Edit User')),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('iban', models.CharField(max_length=255)),
                ('bic', models.CharField(max_length=255)),
                ('amount', models.FloatField(default=0.0)),
                ('bank_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BankAccount')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualBankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_tag_name', models.CharField(max_length=100)),
                ('balance', models.FloatField(default=0.0)),
                ('percentage_of_amount', models.FloatField(blank=True, null=True)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.BankAccount')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.VirtualBankAccount'),
        ),
    ]
