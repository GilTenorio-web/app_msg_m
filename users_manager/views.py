from typing import List
from users_manager.models import Archivo, CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users_manager.forms import FormArchivos, ProfileForm
import joblib
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView

# Create your views here.
def index(request):
    return render(request,"index.html",{"home":"active"})


def profile_form(request):
    if request.method == 'POST':
        form=ProfileForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request,"index.html",{"home":"active"})

    else:
        form=ProfileForm()
    return render(request,"profile-form.html",{"login":"active", "form":form})


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
    pred = predecir(text)
    context = {'text': text, 'pred': pred}
    
    return render(request, "resultado.html", context)


def modelo(request):
    return render(request, "modelo.html") #esta vista renderiza el archivo modelo.html 

@login_required()
def entrada(request):
     
    if request.method == 'POST':
       form = FormArchivos(request.POST, request.FILES)
       messages = 'Error: '
       if form.is_valid():
            print(id)
            form.save()  
            return redirect('listaArchivos')
       else:
            messages.error(request, "Error al procesar el formulario")
    else:
       form = FormArchivos()
    return render(request,'FormArchivos.html',{'form':form})

@login_required()
def file_list(request):
    id_user = request.session['_auth_user_id']
    #us = CustomUser.objects.filter(user = id_user)
    #print(us)
    #files = Archivo.objects.all()
    files = Archivo.objects.filter(user__user= id_user)
    contexto = {'files': files}

    return render(request, 'listaFiles.html',contexto)

def file_classifier(request,id_file):
    file = Archivo.objects.get(id = id_file)
    
    
    return render(request, "classifier.html", {'id': id_file})

def file_delete(request,id_file):
    f = Archivo.objects.get(id=id_file)
    if request.method == 'POST':
        f.delete()
        return redirect('listaArchivos')
    return render(request,"file_delete.html",{'file':f}) 





