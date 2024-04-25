from django.urls import path
from . import views

handler404 = 'page.views.custom_404'

urlpatterns = [
    path('', views.home, name='home'),
    path('startServer/<game>', views.startServer, name='startBot'),
    path('stopServer/<game>', views.stopServer, name='stopBot'),
    path('botStatus/', views.serverStatus, name='botStatus'),
    path('startBot/', views.startBot),
    path('stopBot/', views.stopBot),
]
