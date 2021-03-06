# Generated by Django 3.1.1 on 2020-09-29 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KarunaCurrent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='date')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('description', models.CharField(max_length=300)),
                ('receipt', models.ImageField(upload_to='', verbose_name='Photo of receipt')),
                ('transaction_id', models.CharField(max_length=30)),
                ('transaction_status', models.CharField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Received', 'Received')], max_length=10, verbose_name='Transaction status')),
                ('transaction_type', models.CharField(choices=[('UPI', 'UPI'), ('Band', 'Bank'), ('Credit', 'Credit')], max_length=10, verbose_name='Transaction type')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linked_wallet', to='wallet.wallet', verbose_name='Linked wallet')),
            ],
        ),
    ]
