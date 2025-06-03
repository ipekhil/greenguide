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
    path("edit/<int:plant_id>/", views.edit_plant_type, name="edit_plant_type"),

    path("delete/<int:id>/", views.delete_plant_type, name="delete_plant_type"),
    path("myplants/", views.user_plants, name="user_plants"),
    path("myplants/<int:id>/delete/", views.delete_user_plant, name="delete_user_plant"),

    path("alerts/", views.all_alerts, name="all_alerts"),

    path("myplants/<int:pk>/", views.user_plant_detail, name="user_plant_detail"),

]
