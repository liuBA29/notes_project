from django.urls import path
from .views import *

urlpatterns = [
    path('', client_list, name='client_list'),
    path('<int:pk>/', client_detail, name='client_detail'),

    path('add/', add_client, name='add_client'),
    path('<int:pk>/edit/', edit_client, name='edit_client'),
    path('<int:pk>/delete/', delete_client, name='delete_client'),

    path('api/asterisk_status/', asterisk_status, name='asterisk_status'),
    path('calls/', call_list, name='call_list'),
]
