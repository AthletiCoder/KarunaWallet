# Generated by Django 3.1.1 on 2020-10-02 08:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_karunacurrent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='peak_balance',
        ),
        migrations.AddField(
            model_name='karunacurrent',
            name='approved_timestamp',
            field=models.DateTimeField(null=True, verbose_name='Approved time'),
        ),
        migrations.AddField(
            model_name='karunacurrent',
            name='received_timestamp',
            field=models.DateTimeField(null=True, verbose_name='Received time'),
        ),
        migrations.AddField(
            model_name='karunacurrent',
            name='submitted_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Submitted time'),
        ),
        migrations.AddField(
            model_name='wallet',
            name='karuna_tally',
            field=models.IntegerField(default=0, verbose_name='Total Karuna tally'),
        ),
        migrations.AlterField(
            model_name='karunacurrent',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date'),
        ),
    ]