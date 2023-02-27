from django.shortcuts import render,redirect
from crazymix.models import User

# from .forms import UserForm
from .forms import LoginForm,RegisterForm
#from forms import LoginForm
#from .models import User
from django_mongoengine.mongo_auth.managers import UserManager
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

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
    #form = UserForm()
    return render(request,'registration/signup.html', {'title':"S'inscrire"})
    # return render(request,'crazymix/inscription.html', {'title':"S'inscrire", 'form' : form})

def compte(request):
    return render(request,'crazymix/compte.html', {'title':'Mon compte'})

def infos(request):
    return render(request,'crazymix/infos.html', {'title':'Informations sur le site du studio'})


def login(request):

    if (request.method =="POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            # pwd=password
            # hashed_password = make_password(pwd)
            # if check_password('password', hashed_password):
            user=User.objects.filter(username=username).first()

            # user = authenticate(request, username=username, password=password)
            # si la liste n'est pas vide donc il a trouvé un user avec le username et le pwd'
            if user is None:
                # return redirect('login')
                return render(request, 'registration/login.html', {'form': form})
            else:
                if check_password(password, user.password):
                    return redirect('compte')
    else:
        # user=User(username='admin',password= make_password('12345qwe!'))
        # user.save()
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if(request.method=="POST"):
        form = RegisterForm(request.POST,request.FILES)

        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            id=form.cleaned_data['id']
            email = form.cleaned_data['email']
            spotify = form.cleaned_data['spotify']
            instagram = form.cleaned_data['instagram']
            description = form.cleaned_data['description']
            avatar = form.cleaned_data['avatar']
            role = form.cleaned_data['role']
            password = form.cleaned_data['passwor']

            #user=User(first_name=first_name,last_name=last_name,id=id,email=email,spotify=spotify,
            #                 instagram=instagram,description=description,avatar=avatar,role=role,password=password,)

            #user.save()
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def sessionUser(request):
    user_id=request.session.get('user_id')
    if user_id is not None:
        user = User.objects.get(pk=user_id)
    else:
        return redirect ('login')