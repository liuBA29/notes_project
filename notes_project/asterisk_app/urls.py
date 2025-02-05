from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('<int:pk>/', views.client_detail, name='client_detail'),

    path('add/', views.add_client, name='add_client'),
    path('<int:pk>/edit/', views.edit_client, name='edit_client'),
    path('<int:pk>/delete/', views.delete_client, name='delete_client'),

    path('asterisk/', views.check_asterisk_connection, name='asterisk'),
    path('calls/', views.call_list, name='call_list'),
]
