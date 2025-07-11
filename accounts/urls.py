from django.urls import path
from accounts import views

urlpatterns = [
    path('login/' , views.login_page, name='login_page'),
    path('register/' , views.register, name='register'),
    path('send_otp/<email>/' , views.send_otp, name='send_otp'),
    path('verify-otp/<email>/' , views.verify_otp, name='verify_otp'),


    path('verify-account/<token>',views.verifyEmail , name="verifyEmail"),


    path('login-vendor/' , views.login_vendor, name='login_vendor'),
    path('register-vendor/' , views.register_vendor, name='register_vendor'),
    path('send_otp_vendor/<email>/' , views.send_otp_vendor, name='send_otp'),
    path('verify-otp_vendor/<email>/' , views.verify_otp_vendor, name='verify_otp'),
    path('verify-account_vendor/<token>',views.verifyEmail_vendor , name="verifyEmail"),




     path('dashboard/', views.dashboard , name="dashboard"),

     path('logout-user/',views.logout_user,name="logout_user"),
    path('logout-vendor/',views.logout_vendor,name="logout_vendor"),


    path('add-hotel/', views.add_hotel , name="add_hotel"),

     path('delete_image/<id>/' , views.delete_image , name="delete_image"),

    path('upload-images/<slug>/', views.upload_images , name="upload_images"),

path('edit-hotel/<slug>/', views.edit_hotel , name="edit_hotel"),

]