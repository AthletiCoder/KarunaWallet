# Generated by Django 3.1.1 on 2020-09-28 20:42

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
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0, verbose_name='Karuna balance')),
                ('peak_balance', models.IntegerField(default=models.IntegerField(default=0, verbose_name='Karuna balance'), verbose_name='Peak Karuna Balance')),
                ('account_number', models.CharField(max_length=20, null=True, unique=True, verbose_name='Account number')),
                ('ifsc_code', models.CharField(max_length=20, null=True, verbose_name='IFSC code')),
                ('mobile_number', models.CharField(max_length=10, unique=True, verbose_name='Mobile number')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_owner', to=settings.AUTH_USER_MODEL, verbose_name='Account owner')),
            ],
        ),
    ]
