from typing import List
from users_manager.models import Archivo, CustomUser, Room, Message
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users_manager.forms import FormArchivos, ProfileForm
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView
import tkinter as tk
from tkinter import filedialog
import os

from django.http import HttpResponse, JsonResponse
"""Instalar las siguientes librerias"""
import joblib
import json

# Create your views here.
def index(request):
    return render(request,"index.html", {"home":True, "user_loged":False})


def index_loged(request):
    return render(request,"index.html", {"home":True, "user_loged":True})


def profile_form(request):
    if request.method == 'POST':
        form=ProfileForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request,"index.html", {"home":True, "newUser":2})
        else:
            return render(request,"index.html", {"home":True, "newUser":1})

    else:
        form=ProfileForm()

    return render(request,"profile-form.html",{"form":form})


class UserSignUp(CreateView):
    model = User
    template_name = 'new_login.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('profile-form')


#Vistas del modelo
def clasificador(request):
    def predecir(texto):
        """
        Esta función carga el modelo entrenado y el vector, el modelo tiene una exactitud del 79%
        Recibe un String
        Retorna 0 si el texto lo clasifica como no ofensivo y 1 si lo clasifica como ofensivo
        """
        modelo = joblib.load('users_manager/research/modeloEntrenado.pkl')
        vector = joblib.load('users_manager/research/vector.pkl')

        matriz = vector.transform([texto])
        return modelo.predict(matriz)
    text = request.GET["tweet"]
    #Hacemos la prediccion de los datos ingresados 
    id_user = request.session['_auth_user_id']
    files = Archivo.objects.filter(user__user = id_user)
    pred = predecir(text)
    context = {'text': text, 'pred': pred, 'files':files, "user_loged":True, "misCnvs":"active"}
    
    return render(request, "resultado.html", context)


def modelo(request):
    id_user = request.session['_auth_user_id']
    files = Archivo.objects.filter(user__user = id_user)
    contexto = {'files':files, "user_loged":True, "misCnvs":"active"}

    return render(request, "modelo.html", contexto) #esta vista renderiza el archivo modelo.html 


@login_required()
def entrada(request):
     
    if request.method == 'POST':
       form = FormArchivos(request.POST, request.FILES)
       messages = 'Error: '
       if form.is_valid():
            form.save()  
            return redirect('listaArchivos')
       else:
            messages.error(request, "Error al procesar el formulario")
    else:
        id_user = request.session['_auth_user_id']
        files = Archivo.objects.filter(user__user = id_user)
        form = FormArchivos()
        contexto = {'form':form, 'files':files, "user_loged":True, "misCnvs":"active"}
    return render(request,'FormArchivos.html',contexto)


@login_required()
def file_list(request):

    id_user = request.session['_auth_user_id']
    files = Archivo.objects.filter(user__user = id_user)
    contexto = {'files':files, "user_loged":True, "misCnvs":"active"}

    return render(request, 'listaFiles.html',contexto)


def file_classifier(request,id_file):
    class mensaje:
        
        def __init__(self,message,user, predict = None):
            self.message = message
            self.user = user
            self.predict = predict

    def predecir(texto):
        """
        Esta función carga el modelo entrenado y el vector, el modelo tiene una exactitud del 79%
        Recibe un String
        Retorna 0 si el texto lo clasifica como no ofensivo y 1 si lo clasifica como ofensivo
        """
        modelo = joblib.load('users_manager/research/modeloEntrenado.pkl')
        vector = joblib.load('users_manager/research/vector.pkl')

        matriz = vector.transform([texto])
        return modelo.predict(matriz)
    
    file = Archivo.objects.get(id = id_file).file
    file_name = Archivo.objects.get(id = id_file).name
    
    lista =list()
    name = set()
    agressive = 0
    noAgressive = 0

    with file.open(mode='rb') as contenido:
        datos = json.load(contenido)

        for m in datos['messages']:
            objetoMessage =  mensaje(m['value'],m['user'])
            message = m['value']
            pre =predecir(message)
            objetoMessage.predict = pre
            lista.append(objetoMessage)
            name.add(m['user'])
            if pre == 1:
                agressive += 1
            else:
                noAgressive += 1
    
    user1_NoAgressive = 0
    user1_Agressive = 0
    user2_NoAgressive = 0
    user2_Agressive = 0
    users = list(name)

    for u in lista:
        if u.user == users[0]:
            if u.predict == 0:
                user1_NoAgressive += 1
            else:
                user1_Agressive += 1
        else:
            if u.predict == 0:
                user2_NoAgressive += 1
            else:
                user2_Agressive += 1 
    

    labelsGeneral = []
    dataGeneral = []
    labelsGeneral.append('Agresivos')
    labelsGeneral.append('No Agresivos')
    dataGeneral.append(agressive)
    dataGeneral.append(noAgressive)

    labelsUser1 = []
    dataUser1 = []
    labelsUser1.append('Agresivos')
    labelsUser1.append('No Agresivos')
    dataUser1.append(user1_Agressive)
    dataUser1.append(user1_NoAgressive)

    labelsUser2 = []
    dataUser2 = []
    labelsUser2.append('Agresivos')
    labelsUser2.append('No Agresivos')
    dataUser2.append(user2_Agressive)
    dataUser2.append(user2_NoAgressive)            
        
    context = { 'lista': lista, 'labelsG': labelsGeneral, 'dataG':dataGeneral,'file_name':file_name,
                'labelsU1': labelsUser1, 'dataU1': dataUser1, 'labelsU2': labelsUser2, 'dataU2': dataUser2,
                'users': users, 'user_loged':True, 'misCnvs':True, 'clasifier':True}
    
    return render(request, "classifier.html", context)


def file_delete(request,id_file):

    id_user = request.session['_auth_user_id']
    files = Archivo.objects.filter(user__user = id_user)
    f = Archivo.objects.get(id=id_file)
    contexto = {'file':f,'files':files, "user_loged":True, "misCnvs":True}
    if request.method == 'POST':
        f.delete()
        return redirect('listaArchivos')

    return render(request,"file_delete.html",contexto) 


def ingreso_chat(request):
    return render(request, 'ingreso_chat.html', {"user_loged":True, "chat":True})


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'user_loged': True,
        'chat': True
    })


usp = ""
def checkview(request):
    global usp 
    room = request.POST['room_name']
    username = request.POST['username']
    usp = username

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def guardarConv(request, room):
    raiz = tk.Tk()
    raiz.withdraw()
    direccion = filedialog.asksaveasfilename(title = "Guardar Chat")
    raiz.destroy()
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    dict_msgs = {"messages":list(messages.values('user','value'))}
    global usp
    if not direccion:

        return redirect('/'+room+'/?username='+usp )
    else:

        with open(direccion, 'w') as outfile:
            json.dump(dict_msgs, outfile)
        return redirect('/'+room+'/?username='+usp )