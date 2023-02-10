from django.shortcuts import render

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
    return render(request,'crazymix/inscription.html', {'title':"S'inscrire"})

def compte(request):
    return render(request,'crazymix/compte.html', {'title':'Mon compte'})

def infos(request):
    return render(request,'crazymix/infos.html', {'title':'Informations sur le site du studio'})
