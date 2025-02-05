import os
from dotenv import load_dotenv
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ClientForm
from .scripts.asteriisk_connection import AsteriskConnection

host = os.getenv('ASTERISK_HOST')  # IP-адрес сервера
port = int(os.getenv('ASTERISK_PORT', 22))  # Преобразуем порт в число
username = os.getenv('ASTERISK_USERNAME')  # Имя пользователя для подключения
password = os.getenv('ASTERISK_PASSWORD')  # Пароль для подключения
load_dotenv()


def check_asterisk_connection(request):
    # Получаем данные для подключения из настроек или переменных окружения

    # Создаем объект подключения к Asterisk
    asterisk_conn = AsteriskConnection(host, port, username, password)

    # Подключаемся к серверу Asterisk
    asterisk_conn.connect()

    # Проверяем соединение и передаем результат в шаблон
    is_connected = asterisk_conn.check_connection()

    # Закрываем соединение после проверки
    asterisk_conn.close_connection()

    # Отправляем результат в контекст шаблона
    context = {
        'is_connected': is_connected,
    }

    return render(request, 'asterisk_app/asterisk_con.html', context)



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

