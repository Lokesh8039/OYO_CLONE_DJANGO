from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import Hotel,HotelUser,HotelBooking,Ameneties
from django.contrib import messages
from datetime import datetime


def index(request):
    hotels = Hotel.objects.all()
   

    if request.GET.get('search'):
        hotels = hotels.filter(hotel_name__icontains = request.GET.get('search'))
    try:
        hotel_user = HotelUser.objects.get(id=request.user.id)
        user_name = hotel_user.first_name
    except HotelUser.DoesNotExist:
        user_name = "Guest"
    if request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
        if sort_by == "sort_low":
            hotels = hotels.order_by('hotel_offer_price')
        elif sort_by == "sort_high":
            hotels = hotels.order_by('-hotel_offer_price')
    
    return render(request, 'index.html', context = {'hotels' : hotels[:50],'user':user_name})



def hotel_details(request, slug):
    hotel = Hotel.objects.get(hotel_slug = slug)

    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date = datetime.strptime(start_date , '%Y-%m-%d')
        end_date = datetime.strptime(end_date , '%Y-%m-%d')
        days_count = (end_date - start_date).days

        if days_count <= 0:
            messages.warning(request, "Invalid Booking Date.")

            return HttpResponseRedirect(request.path_info)


        HotelBooking.objects.create(
            hotel = hotel,
            booking_user = HotelUser.objects.get(id = request.user.id),
            booking_start_date = start_date,
            booking_end_date =end_date,
            price = hotel.hotel_offer_price * days_count
        )
        messages.warning(request, "Booking Captured.")

        return HttpResponseRedirect(request.path_info)


    return render(request, 'hotel_detail.html', context = {'hotel' : hotel})