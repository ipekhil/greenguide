from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.register, name="register"),

    path("login/",
         auth_views.LoginView.as_view(template_name="plants/login.html"),
         name="login"),

    path("logout/",
         auth_views.LogoutView.as_view(),
         name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("delete/<int:id>/", views.delete_plant_type, name="delete_plant_type"),

]
