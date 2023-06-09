from . import views

from django.urls import path,include
from django.contrib.auth import views as auth_views

app_name = 'frontoffice'

urlpatterns = [
    path('', views.home_view, name='home'),
    
  
    path('my-login/', views.login_view, name='login'),
    path('my-logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('get-engagements/', views.get_engagements, name='get_engagements'),

]
