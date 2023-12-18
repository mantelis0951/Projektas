import decimal
from decimal import Decimal
from django.contrib import admin
from .models import Client, Vehicle, RentalContract, Payment, CarReview, Profilis


class RentalContractAdmin(admin.ModelAdmin):
    list_display = ('client', 'vehicle', 'start_date', 'end_date', 'total_cost')

    search_fields = ('id', 'client__first_name', 'client__last_name', "vehicle__model")

    def total_cost(self, obj):
        # Calculate total cost based on associated vehicle, considering deposit
        if obj.vehicle:
            rental_period = (obj.end_date - obj.start_date).days
            rental_price = float(obj.vehicle.rental_price)
            deposit = float(obj.vehicle.deposit)
            total_cost = (rental_period * rental_price) + deposit
            return total_cost
        return None

    total_cost.short_description = 'Total Cost'




class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'personal_code', 'contact_number')
    search_fields = ('first_name', 'last_name', 'personal_code', 'contact_number')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('rental_contract', 'amount', 'payment_date')
    search_fields = ('rental_contract__client__first_name', 'rental_contract__client__last_name', 'amount', 'payment_date')


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'year', 'rental_price','deposit', 'get_status_display')
    search_fields = ('manufacturer', 'model', 'year')


class CarReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'reviewer', 'date_created', 'content')


admin.site.register(RentalContract, RentalContractAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CarReview, CarReviewAdmin)
admin.site.register(Profilis)
