import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Hotel

def generateRandomToken():
    return str(uuid.uuid4())



def sendEmailToken(email, token):
    subject = "Verify Your Email Address"
    message = f"""Hi, please verify your email account by clicking this link: 
    https://oyo-clone-django-2.onrender.com/account/verify-account/{token}
    """

    send_mail(subject,message,settings.EMAIL_HOST_USER,[email],fail_silently=False)

def sendEmailToken_vendor(email, token):
    subject = "Verify Your Email Address"
    message = f"""Hi, please verify your email account by clicking this link: 
    https://oyo-clone-django-2.onrender.com/account/verify-account_vendor/{token}
    """

    send_mail(subject,message,settings.EMAIL_HOST_USER,[email],fail_silently=False)

    
def sendOTPtoEmail(email , otp):
    subject = "OTP for Account Login"
    message = f"""Hi, use this OTP to login
     {otp} 
    
    """
    send_mail(
       subject,
       message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )




def generateSlug(hotel_name):
    slug = f"{slugify(hotel_name)}-" + str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug = slug).exists():
        return generateSlug(hotel_name)
    return slug
  
