from django.urls import path
from . import views

urlpatterns = [
    path('add_turf/', views.add_turf),
    path('view_turf/', views.view_turf),
    path('update_turf/<int:id>/', views.update_turf),
    path('delete_turf/<int:id>/', views.delete_turf),
    path('add_booking/', views.add_booking),
    path('view_booking/', views.view_booking),
    path('cancel_booking/<int:id>/', views.cancel_booking),
    path('single_booking/<int:id>/', views.single_booking),
    path('register_user/', views.register_user),
    path('login_user/', views.login_user),
]