from django.contrib import admin
from django.urls import path
from headapp import views,apiview,mobileapiviews
from django.conf import settings  
from django.conf.urls.static import static  


urlpatterns = [
    # ---- Web Routes ----
    path('',views.home_view),
    path('adminlogin',views.admin_login_view),
    path('adminpanel/users',views.adminpanel_users_view),
    path('adminpanel/radio_content',views.radio_content_view),
    
    # ---- WEB API ROUTES ----
    path('api/add_section',apiview.add_section_apiview),
    path('api/sections_content/<tab_id>',apiview.sections_content_apiview),
    
    # ---- MOBILE API ROUTES ----
    path('api/forgot_password',mobileapiviews.forgotpassword_apiview),
    path('api/fetch_content',mobileapiviews.fetch_content_apiview),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  





