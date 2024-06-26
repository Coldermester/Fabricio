from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("crud/", views.car_list, name="crud"),
]
