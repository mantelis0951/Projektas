# models.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.models import AbstractUser
from PIL import Image

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    personal_code = models.CharField(max_length=11, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('car', 'Automobilis'),
        ('motorcycle', 'Motociklas'),
    ]
    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Statusas',
    )

    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    engine_type = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    engine_capacity = models.FloatField()
    body_type = models.CharField(max_length=50)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.end_date and date.today() > self.end_date:
            return True
        return False

    def __str__(self):
        return f"{self.id},{self.client} - {self.start_date} to {self.end_date}"

    def calculate_total_cost(self):
        rental_period = (self.end_date - self.start_date).days
        total_cost = rental_period * float(self.vehicle.rental_price)
        return total_cost

    photo1 = models.ImageField(upload_to='vehicle_photos', null=True, blank=True)
    photo2 = models.ImageField(upload_to='vehicle_photos', null=True, blank=True)
    photo3 = models.ImageField(upload_to='vehicle_photos', null=True, blank=True)
    photo4 = models.ImageField(upload_to='vehicle_photos', null=True, blank=True)

    def __str__(self):
        return f"{self.year} {self.manufacturer} {self.model}"


class RentalContract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)




class Payment(models.Model):
    rental_contract = models.ForeignKey(RentalContract, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"{self.rental_contract} - {self.payment_date}"


class CarReview(models.Model):
    car = models.ForeignKey('Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']

class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

