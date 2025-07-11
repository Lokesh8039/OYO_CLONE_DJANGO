from home import views
from django.urls import path

urlpatterns = [
    path('',views.index , name="index"),
     path('hotel-details/<slug>/', views.hotel_details, name="hotel_details"),
]
