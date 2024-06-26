# from authuser.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CarForm, CustomAuthenticationForm, CustomUserCreationForm
from .models import Car, User


def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "index.html", {"username": username})


def cadastro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, email=email, password=raw_password)
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "cadastro.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


def car_list(request):
    cars = Car.objects.all()
    return render(request, "cars_list.html", {"cars": cars})


def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            return JsonResponse({"id": car.id, "name": car.name, "brand": car.brand})
    else:
        form = CarForm()
    return render(request, "car_form.html", {"form": form})


def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return JsonResponse({"id": car.id, "name": car.name, "brand": car.brand})
    else:
        form = CarForm(instance=car)
    return render(request, "car_form.html", {"form": form})


def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        car.delete()
        return JsonResponse({"message": "Carro excluído com sucesso!"})
    return JsonResponse({"error": "Ocorreu um erro ao excluir o carro."}, status=400)
