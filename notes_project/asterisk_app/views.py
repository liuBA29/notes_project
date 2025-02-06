import os
from dotenv import load_dotenv
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import threading
import time
from .models import *
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ClientForm
from .scripts.asterisk_connection import AsteriskConnection
from .scripts.calling_number import calling_number

# Глобальная переменная для хранения статуса


host = os.getenv('ASTERISK_HOST')  # IP-адрес сервера
port = int(os.getenv('ASTERISK_PORT', 22))  # Преобразуем порт в число
username = os.getenv('ASTERISK_USERNAME')  # Имя пользователя для подключения
password = os.getenv('ASTERISK_PASSWORD')  # Пароль для подключения
load_dotenv()



def asterisk_status(request):
    asterisk_conn = AsteriskConnection(host, port, username, password)
    asterisk_conn.connect()

    status = asterisk_conn.check_connection()
    if status:
        active_calls = asterisk_conn.get_active_calls()
        calling_numbers = calling_number.get_active_calls().get('calling_numbers', [])

    else:
        active_calls = "no asterisk connection"
        calling_numbers = []

    # Дополнительно получаем клиентов, чьи номера совпадают с номерами звонящих
    clients = Client.objects.all()
    client_names = []

    for client in clients:
         # Сопоставляем номера клиентов с их именами
        if client.contact_info and client.contact_info.phone:
            for number in calling_numbers:
                if number == client.contact_info.phone:
                    client_names.append(client.name)

    # Возвращаем JSON с добавленным именем клиента, если номер совпал
    return JsonResponse({
        'asterisk_status': status,
        'active_calls': active_calls,
        'calling_numbers': calling_numbers,
        'client_names': client_names  # Добавляем пары "номер звонящего": "имя клиента"
    })





def client_list(request):
    #clients = Client.objects.all().values('id', 'name', 'is_active')
    clients = Client.objects.all()
    context = {
        'clients': clients,
    }
    #return JsonResponse(list(clients), safe=False)
    return render(request, 'asterisk_app/client_list.html', context)


def client_detail(request, pk):

    clients = Client.objects.all()
    client = get_object_or_404(Client, pk=pk)
    context = {

        'clients': clients,
        'client': client,
    }
    return render(request, 'asterisk_app/client_detail.html', context)

# Страница добавления клиента
def add_client(request):
    clients = Client.objects.all()
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()

    context = {
        'form': form,
        'clients': clients,
    }
    return render(request, 'asterisk_app/add_client.html', context)


def edit_client(request, pk):

    clients = Client.objects.all()
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form=ClientForm(instance=client)
    context = {
        'form': form,

        'clients': clients,
        'client': client,
    }
    return render(request, 'asterisk_app/add_client.html', context)

def delete_client(request, pk):
    clients = Client.objects.all()
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()  # Удаляем клиента
        # messages.success(request, f"Client {client.name} successfully deleted.")
        return redirect('client_list')  # Перенаправляем на список клиентов
    context = {

        'clients': clients,
        'client': client,
    }
    return render(request, 'configurations/delete_client.html', context)


def call_list(request):
    calls = CallRecord.objects.all()
    context = {
        'calls': calls,
    }
    return render(request, 'asterisk_app/call_list.html', context)

