from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


# Create your views here.
def index(request):
    return render(request,"index.html",{"home":"active"})


def login(request):
    if request.method == 'POST':
        form=ProfileForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request,"index.html",{"home":"active"})

    else:
        form=ProfileForm()

    return render(request,"login.html",{"login":"active","form":form})

class UserSignUp(CreateView):
    model = User
    template_name = 'new_login.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')