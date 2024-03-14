from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('startServer/<game>', views.startServer, name='startBot'),
    path('stopServer/<game>', views.stopBot, name='stopBot'),
    path('botStatus/', views.botStatus, name='botStatus')
]
