# Generated by Django 2.0.7 on 2018-09-22 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20180922_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharingUserBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sharing_balance', models.FloatField(default=0.0)),
            ],
        ),
        migrations.RemoveField(
            model_name='sharinguser',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='sharinguser',
            name='sharing_group',
        ),
        migrations.RemoveField(
            model_name='sharinguser',
            name='user',
        ),
        migrations.AddField(
            model_name='sharinggroup',
            name='users',
            field=models.ManyToManyField(to='core.Profile'),
        ),
        migrations.AlterField(
            model_name='sharingspending',
            name='paying_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.SharingUserBalance'),
        ),
        migrations.DeleteModel(
            name='SharingUser',
        ),
        migrations.AddField(
            model_name='sharinguserbalance',
            name='sharing_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.SharingGroup'),
        ),
        migrations.AddField(
            model_name='sharinguserbalance',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Profile'),
        ),
    ]