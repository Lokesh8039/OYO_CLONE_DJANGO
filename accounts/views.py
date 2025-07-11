from django.shortcuts import render,redirect ,HttpResponse,HttpResponseRedirect
from .models import HotelUser , HotelVendor,Hotel,Ameneties,HotelImages
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken,sendEmailToken,sendOTPtoEmail,sendEmailToken_vendor,generateSlug
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators import login_required
import random
def login_page(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'hoteluser'):
            return redirect("/")
        else:
            logout(request)
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        hotel_user = HotelUser.objects.filter(email = email)
        if not hotel_user.exists():
            messages.warning(request, "Account Not Found")
            return redirect("login_page")
        if not hotel_user[0].is_verified:
            messages.warning(request, "Account Not Verified")
            return redirect("login_page")
        hotel_user = authenticate(username=hotel_user[0].username,password = password)
        if hotel_user:
            messages.success(request, "Account Login Success")
            login(request,hotel_user)
            return redirect("/")
        messages.warning(request, "Account Password is Wrong")
        return redirect("login_page")

    return render(request , "login.html")



def register(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone_number=request.POST.get('phone_number')
        
        hotel_user = HotelUser.objects.filter(Q(email = email) | Q(phone_number = phone_number))
        if hotel_user.exists():
            messages.warning(request, "Your account exists with This Phone Number and Email")
            return redirect("register")
        hotel_user=HotelUser.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email= email,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()
        sendEmailToken(email,hotel_user.email_token)
        messages.success(request, "Account Created.Email Sent to your mail")
        return redirect("register")
    return render(request , "register.html")


def verifyEmail(request,token):
    try:
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email Verified.Please Login")
        return redirect("login_page")
    except Exception as e:
        return HttpResponse(request , "Token INVALID")
    



def send_otp(request, email):
    hotel_user = HotelUser.objects.filter(
            email = email)
    if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/account/login/')
    if not hotel_user[0].is_verified:
        messages.warning(request, "Account Not Verified")
        return redirect("login_vendor")     

    otp =  random.randint(1000 , 9999)
    hotel_user.update(otp =otp)

    sendOTPtoEmail(email , otp)
    return redirect(f'/account/verify-otp/{email}/')

def verify_otp(request , email):
    if request.method == "POST":
        otp  = request.POST.get('otp')
        hotel_user = HotelUser.objects.get(email = email)

        if otp == hotel_user.otp:
            messages.success(request, "Login Success")
            login(request , hotel_user)
            return redirect('/account/login/')

        messages.warning(request, "Wrong OTP")
        return redirect(f'/account/verify-otp/{email}/')

    return render(request , 'verify_otp.html')


def login_vendor(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'hotelvender'):
            return redirect("dashboard")
        else:
            logout(request)
        
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        hotel_user = HotelVendor.objects.filter(username = email)
        if not hotel_user.exists():
            messages.warning(request, "Account Not Found")
            return redirect("login_vendor")
        if not hotel_user[0].is_verified:
            messages.warning(request, "Account Not Verified")
            return redirect("login_vendor")
        hotel_user = authenticate(username=hotel_user[0].username,password = password)
        if hotel_user:
            messages.success(request, "Account Login Success")
            login(request,hotel_user)
            return redirect("dashboard")
        messages.warning(request, "Incorrect Password")
        return redirect("login_vendor")

    return render(request , "vendor/login_vendor.html")



def register_vendor(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone_number=request.POST.get('phone_number')
        
        hotel_user = HotelVendor.objects.filter(Q(username = email) | Q(phone_number = phone_number))
        if hotel_user.exists():
            messages.warning(request, "Your account exists with This Phone Number and Email")
            return redirect("register_vendor")
        hotel_user=HotelVendor.objects.create(
            username = email,
            first_name = first_name,
            last_name = last_name,
            business_name = business_name,
            email= email,
            phone_number = phone_number,
            email_token = generateRandomToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()
        sendEmailToken_vendor(email,hotel_user.email_token)
        messages.success(request, "Email Sent to your mail")
        return redirect("register_vendor")
    return render(request , "vendor/register_vendor.html")



def send_otp_vendor(request, email):
    hotel_user = HotelVendor.objects.filter(
            username = email)
    if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/account/login/')
    if not hotel_user[0].is_verified:
        messages.warning(request, "Account Not Verified")
        return redirect("login_vendor")

    otp =  random.randint(1000 , 9999)
    hotel_user.update(otp =otp)

    sendOTPtoEmail(email , otp)
    return redirect(f'/account/verify-otp_vendor/{email}/')

def verify_otp_vendor(request , email):
    if request.method == "POST":
        otp  = request.POST.get('otp')
        hotel_user = HotelVendor.objects.get(username = email)

        if otp == hotel_user.otp:
            messages.success(request, "Login Success")
            login(request , hotel_user)
            return redirect('login_vendor')

        messages.warning(request, "Wrong OTP")
        return redirect(f'/account/verify-otp_vendor/{email}/')

    return render(request , 'vendor/verifyotp.html')



def verifyEmail_vendor(request,token):
    try:
        hotel_user = HotelVendor.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email Verified.Please Login")
        return redirect("login_vendor")
    except Exception as e:
        return HttpResponse(request , "Token INVALID")
    



@login_required(login_url='login_vendor')
def dashboard(request):
    context = {'hotels' : Hotel.objects.filter(hotel_owner = request.user)}
    return render(request, 'vendor/vendor_dashboard.html', context)



def logout_user(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect("login_page")



def logout_vendor(request):
    logout(request)
    return redirect("login_vendor")






@login_required(login_url='login_vendor')
def add_hotel(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties= request.POST.getlist('ameneties')
        hotel_price= request.POST.get('hotel_price')
        hotel_offer_price= request.POST.get('hotel_offer_price')
        hotel_location= request.POST.get('hotel_location')
        hotel_slug = generateSlug(hotel_name)

        hotel_vendor = HotelVendor.objects.get(id = request.user.id)

        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor
        )

        for ameneti in ameneties:
            ameneti = Ameneties.objects.get(id = ameneti)
            hotel_obj.ameneties.add(ameneti)
            hotel_obj.save()


        messages.success(request, "Hotel Added Sucessfully")
        return redirect('/account/dashboard/')


    ameneties = Ameneties.objects.all()
        
    return render(request, 'vendor/add_hotel.html', context = {'ameneties' : ameneties})


@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    if request.method == "POST":
        image = request.FILES['image']
        print(image)
        HotelImages.objects.create(
        hotel = hotel_obj,
        image = image
        )
        return HttpResponseRedirect(request.path_info)
     
    return render(request, 'vendor/upload_images.html', context = {'images' : hotel_obj.hotel_images.all()})

@login_required(login_url='login_vendor')
def delete_image(request, id):

    hotel_image = HotelImages.objects.get(id = id)
    hotel_image.delete()
    messages.success(request, "Hotel Image deleted")
    return redirect('/account/dashboard/')





@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    if request.method == "POST":
        image = request.FILES['image']
        print(image)
        HotelImages.objects.create(
        hotel = hotel_obj,
        image = image
        )
        return HttpResponseRedirect(request.path_info)

    return render(request, 'vendor/upload_images.html', context = {'images' : hotel_obj.hotel_images.all()})



@login_required(login_url='login_vendor')
def delete_image(request, id):
    print(id)
    print("#######")
    hotel_image = HotelImages.objects.get(id = id)
    hotel_image.delete()
    messages.success(request, "Hotel Image deleted")
    return redirect('/account/dashboard/')






@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
 
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        
        messages.success(request, "Hotel Details Updated")

        return HttpResponseRedirect(request.path_info)

    ameneties = Ameneties.objects.all()
    
    return render(request, 'vendor/edit_hotel.html', context={'hotel': hotel_obj, 'ameneties': ameneties})