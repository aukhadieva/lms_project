# Generated by Django 5.0.6 on 2024-07-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_payment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(verbose_name='дата оплаты'),
        ),
    ]
