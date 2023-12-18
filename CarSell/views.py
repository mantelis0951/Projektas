from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from .forms import CarReviewForm, UserUpdateForm, ProfilisUpdateForm
from .models import Vehicle, RentalContract, Client, Payment, CarReview
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render, get_object_or_404, reverse
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
def index(request):
    all_vehicles = Vehicle.objects.all()
    all_manufacturers = Vehicle.objects.values_list('manufacturer', flat=True).distinct()

    selected_manufacturer = request.GET.get('selected_manufacturer')

    if selected_manufacturer:

        vehicles_by_manufacturer = all_vehicles.filter(manufacturer=selected_manufacturer)
    else:
        vehicles_by_manufacturer = None

    context = {
        'all_vehicles': all_vehicles,
        'all_manufacturers': all_manufacturers,
        'selected_manufacturer': selected_manufacturer,
        'vehicles_by_manufacturer': vehicles_by_manufacturer,
    }

    return render(request, 'index.html', context=context)



def vehicles(request):
    all_vehicles = Vehicle.objects.all()
    all_manufacturers = Vehicle.objects.values_list('manufacturer', flat=True).distinct()

    selected_manufacturer = request.GET.get('selected_manufacturer')

    if selected_manufacturer:
        all_vehicles = all_vehicles.filter(manufacturer=selected_manufacturer)
    #puslapavimas
    page = request.GET.get('page', 1)

    paginator = Paginator(all_vehicles, 3)
    try:
        all_vehicles = paginator.page(page)
    except PageNotAnInteger:
        all_vehicles = paginator.page(1)
    except EmptyPage:
        all_vehicles = paginator.page(paginator.num_pages)
    #puslapavimas virsuje
    context = {
        'all_vehicles': all_vehicles,
        'all_manufacturers': all_manufacturers,
        'selected_manufacturer': selected_manufacturer,
    }
    return render(request, 'vehicles.html', context=context)

@csrf_protect
def vehicle(request, vehicle_id):
    single_vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    rental_contract = RentalContract.objects.filter(vehicle=single_vehicle).first()

    if request.method == 'POST':
        form = CarReviewForm(request.POST)
        if form.is_valid():
            form.instance.car = single_vehicle
            form.instance.reviewer = request.user
            form.save()

    form = CarReviewForm
    car_reviews = single_vehicle.carreview_set.all()
    context = {
        'vehicle': single_vehicle,
        'car_reviews': car_reviews,
        'form': form,
        'rental_contract': rental_contract,
    }
    return render(request, 'vehicle.html', context=context)


def rental_contracts(request):
    all_rental_contracts = RentalContract.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(all_rental_contracts, 3)
    try:
        all_rental_contracts = paginator.page(page)
    except PageNotAnInteger:
        all_rental_contracts = paginator.page(1)
    except EmptyPage:
        all_rental_contracts = paginator.page(paginator.num_pages)

    context = {
        'all_rental_contracts': all_rental_contracts
    }

    return render(request, 'rental_contracts.html', context=context)

def success_page(request):
    return render(request, 'success_page.html')


def search_results(request):
    query = request.GET.get('query')
    results = Vehicle.objects.filter(manufacturer__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payment_list.html', {'payments': payments})

def vehicles_list(request):
    all_vehicles = Vehicle.objects.all()
    return render(request, 'vehicles_list.html', {'all_vehicles': all_vehicles})

@login_required
def user_rentals(request):
    user_rental_list = RentalContract.objects.filter(user=request.user)

    # RIKIAVIAMS
    sort_by = request.GET.get('sort_by', 'end_date')
    user_rental_list = user_rental_list.order_by(sort_by)

    # PUSLAPIACIMAS
    paginator = Paginator(user_rental_list, 5)
    page = request.GET.get('page')

    try:
        user_rentals = paginator.page(page)
    except PageNotAnInteger:
        user_rentals = paginator.page(1)
    except EmptyPage:
        user_rentals = paginator.page(paginator.num_pages)

    context = {
        'user_rentals': user_rentals,
        'sort_by': sort_by,
    }

    return render(request, 'user_rentals.html', context)

@csrf_protect
def register(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']


        if not username or not email or not password or not password2:
            messages.error(request, 'Visi laukai privalo būti užpildyti.')
            return redirect('register')


        if password == password2:

            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:

                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:

                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')

    return render(request, 'registration/register.html')


class CarDetailView(FormMixin, generic.DetailView):
    model = Vehicle
    template_name = 'vehicle.html'
    form_class = CarReviewForm


    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if the request method is POST
        if request.method == 'POST':
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)


    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(CarDetailView, self).form_valid(form)

@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)


class CarByAdminCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    fields = ['vehicle_type','status', 'manufacturer', 'model', 'year', 'color', 'engine_type', 'fuel_type','engine_capacity',
              'body_type', 'rental_price', 'cover', 'deposit', 'photo1','photo2', 'photo3', 'photo4']
    success_url = reverse_lazy('vehicles')
    template_name = 'vehicle_form.html'

    def form_valid(self, form):
        form.instance.reader = self.request.user
        return super().form_valid(form)



class CarByAdminUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    fields = ['vehicle_type','status', 'manufacturer', 'model', 'year', 'color', 'engine_type', 'fuel_type','engine_capacity',
              'body_type', 'rental_price', 'cover', 'deposit', 'photo1','photo2', 'photo3', 'photo4']
    success_url = reverse_lazy('vehicles')
    template_name = 'vehicle_form.html'
    pk_url_kwarg = 'vehicle_id'



    def test_func(self):
        return self.request.user.is_superuser


class CarByAdminDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy('vehicles')
    template_name = 'vehicle_delete.html'
    pk_url_kwarg = 'vehicle_id'

    def test_func(self):
        return self.request.user.is_superuser