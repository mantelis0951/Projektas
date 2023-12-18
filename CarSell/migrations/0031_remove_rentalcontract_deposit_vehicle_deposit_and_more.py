# Generated by Django 4.2.7 on 2023-12-13 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarSell', '0030_profilis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentalcontract',
            name='deposit',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='deposit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='profilis',
            name='nuotrauka',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]
