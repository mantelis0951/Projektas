# Generated by Django 4.2.7 on 2023-12-11 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarSell', '0025_remove_vehicle_additional_images_vehicleimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='additional_images',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='photo1',
            field=models.ImageField(blank=True, null=True, upload_to='vehicle_photos', verbose_name='Nuotrauka 1'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to='vehicle_photos', verbose_name='Nuotrauka 2'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='photo3',
            field=models.ImageField(blank=True, null=True, upload_to='vehicle_photos', verbose_name='Nuotrauka 3'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='photo4',
            field=models.ImageField(blank=True, null=True, upload_to='vehicle_photos', verbose_name='Nuotrauka 4'),
        ),
        migrations.DeleteModel(
            name='VehicleImage',
        ),
    ]
