from django.urls import include, path
from . import views
# from .views import rent_vehicle, success_page
from .views import search_results, CarByAdminCreateView, CarByAdminUpdateView, CarByAdminDeleteView

urlpatterns = [
    path('', views.index, name='index'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('vehicle/<int:vehicle_id>', views.vehicle, name='vehicle'),
    path('vehicles/new', CarByAdminCreateView.as_view(), name='vehicle-new'),
    path('vehicle/<int:vehicle_id>/update', CarByAdminUpdateView.as_view(), name='vehicle-update'),
    path('vehicle/<int:vehicle_id>/delete', CarByAdminDeleteView.as_view(), name='vehicle-delete'),
    path('rental_contracts/', views.rental_contracts, name='rental_contracts'),
    path('clients/', views.client_list, name='clients'),
    path('payments/', views.payment_list, name='payments'),
    path('all_vehicles/', views.vehicles_list, name='all_vehicles'),
    path('success/', views.success_page, name='success_page'),
    path('search/', search_results, name='search_results'),
    path('register/', views.register, name='register'),
    path('user_rentals', views.user_rentals, name='my-rentals'),
    path('profilis/', views.profilis, name='profilis'),

    # path('nuoma/<int:nuoma_detaliau>', views.nuoma_detaliau, name='nuoma_detaliau'),
    # path('rent-vehicle/', rent_vehicle, name='rent_vehicle'),

]