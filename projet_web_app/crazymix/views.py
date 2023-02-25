from django.shortcuts import render,redirect
# from .forms import UserForm
from .forms import LoginForm

# Create your views here.


def index (request):
    return render(request,'crazymix/index.html', {'title':'CrazyMix - Studio'})

def reservation(request):
    return render(request,'crazymix/reservation.html', {'title':"Réserver une session d'enregistrement"})

def sessions(request):
    return render(request,'crazymix/sessions.html', {'title':"Mes sessions d'enregistrement"})

def extraits_artistes(request):
    return render(request,'crazymix/extraits_artistes.html', {'title':'Exraits - Artistes'})

def connexion(request):
    return render(request,'crazymix/connexion.html', {'title':'Se connecter'})

def inscription(request):
    # form = UserForm()
    return render(request,'registration/signup.html', {'title':"S'inscrire", 'form' : form})
    # return render(request,'crazymix/inscription.html', {'title':"S'inscrire", 'form' : form})

def compte(request):
    return render(request,'crazymix/compte.html', {'title':'Mon compte'})

def infos(request):
    return render(request,'crazymix/infos.html', {'title':'Informations sur le site du studio'})


def login(request):
    if (request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})