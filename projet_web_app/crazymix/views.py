from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from django.http import HttpResponse
from crazymix.models import Utilisateur
# from .forms import UserForm
from .forms import LoginForm, RegisterForm, ModifierProfilForm, ModifierInfoPersoForm,ModifierContactForm,ModifierAdresseForm,ModifierMdpForm
import datetime
import base64
# from django_mongoengine.mongo_auth.managers import UserManager
import calendar
from datetime import date
from datetime import datetime
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
    form = ''
    # Date aujourd'hui
    dateNow = datetime.now()
    today = dateNow.day
    heureActuelle = dateNow.hour
    cal = calendar.Calendar(firstweekday=0)
    monthDates = cal.monthdays2calendar(dateNow.year, dateNow.month)

    # Texte
    joursSemaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre",
            "Décembre"]
    heures = []
    for h in range(8, 20):
        classe = None
        if (h <= dateNow.hour):
            classe = 'text-secondary'
        heures.append({'hDebut': h, 'hFin': h + 1, 'classe': classe})

    # Recherche données de la semaine actuelle
    semaine_trouvee = False
    jour_trouve = False
    index_jour = 0
    index_semaine = 0
    while not semaine_trouvee and index_semaine < len(monthDates):
        index_jour = 0
        while not jour_trouve and index_jour < len(monthDates[index_semaine]):
            # 0=date 1=jour_semaine

            if today == monthDates[index_semaine][index_jour][0]:
                jour_trouve = True
            else:
                index_jour = index_jour + 1
        if jour_trouve:
            semaine_trouvee = True
        else:
            index_semaine = index_semaine + 1

    # Recherche des données du mois précédent si se chevauchent
    semainePadding = []
    previousMonthIncluded = False
    nextMonthIncluded = False
    if index_semaine == 0 and monthDates[index_semaine][0][0] == 0:
        previousMonthIncluded = True
        previousMonth = 0
        previousYear = dateNow.year
        if dateNow.month == 1:
            previousYear = dateNow.year - 1
            previousMonth = 12
        else:
            previousMonth = dateNow.month - 1
        paddingMonthDates = cal.monthdays2calendar(previousYear, previousMonth)
        semainePadding = paddingMonthDates[len(paddingMonthDates) - 1]
    elif index_semaine == len(monthDates) - 1 and monthDates[index_semaine][len(monthDates[index_semaine] - 1)] == 0:
        nextMonthIncluded = True
        nextMonth = 0
        nextYear = dateNow.year
        if dateNow.month == 12:
            nextYear = dateNow.year + 1
            nextMonth = 1
        else:
            nextMonth = dateNow.month + 1
        paddingMonthDates = cal.monthdays2calendar(nextYear, nextMonth)
        semainePadding = paddingMonthDates[0]

    # Stockage des dates de la semaine incluant les chevauchements
    semaineActuelle = monthDates[index_semaine]
    datesSemaine = []
    for index in range(7):
        classe = None
        style = None
        if semaineActuelle[index][0] == 0:
            if previousMonthIncluded:
                classe = 'text-secondary'
            datesSemaine.append(
                {'date': semainePadding[index][0], 'jour': joursSemaine[index], 'classe': classe, 'style': style,
                 'heures': heures})

        else:
            if semaineActuelle[index][0] == today:
                style = "background-color: #5a6268;border-radius:7px;"
            elif semaineActuelle[index][0] < today:
                classe = 'text-secondary'
            datesSemaine.append(
                {'date': semaineActuelle[index][0], 'jour': joursSemaine[index], 'classe': classe, 'style': style})

    # Attribution du/des nom(s) de(s) mois de la semaine
    moisSemaine = mois[dateNow.month - 1]
    if previousMonthIncluded:
        moisSemaine = "{0} / {1}".format(mois[previousMonth - 1], moisSemaine)
    elif nextMonthIncluded:
        moisSemaine = "{0} / {1}".format(moisSemaine, mois[nextMonth - 1])

    return render(request, 'crazymix/reservation.html', {'title': "Réserver une session d'enregistrement",
                                                         'form': form, 'jours_semaine': joursSemaine,
                                                         'datesSemaine': datesSemaine,
                                                         'moisSemaine': moisSemaine, 'today': dateNow.day,
                                                         "heureActuelle": dateNow.hour, 'heures':heures})
    # return render(request,'crazymix/reservation.html', {'title':"Réserver une session d'enregistrement"})

def sessions(request):
    return render(request,'crazymix/sessions.html', {'title':"Mes sessions d'enregistrement"})

def extraits_artistes(request):
    return render(request,'crazymix/extraits_artistes.html', {'title':'Exraits - Artistes'})

def connexion(request):
    return render(request,'crazymix/connexion.html', {'title':'Se connecter'})
def deconnexion(request):
    request.session.clear()
    return redirect('index')
def inscription(request):
    #form = UserForm()
    return render(request,'registration/signup.html', {'title':"S'inscrire"})
    # return render(request,'crazymix/inscription.html', {'title':"S'inscrire", 'form' : form})

def compte(request):
    # def authenticate(self, username=None, password=None, **kwargs):
    #     try:
            ab=request.session.get('is_authenticated')

            if 'is_authenticated' in request.session and request.session['is_authenticated']:


                utilisateur_id = request.session['utilisateur_id']
                utilisateur = Utilisateur.objects.get(id=utilisateur_id)
                image_proxy=utilisateur.avatar
                image_bytes = image_proxy.read()
                image_data = base64.b64encode(image_bytes).decode('utf-8')
                image_src = f"data:image/jpeg;base64,{image_data}"


        # except (DoesNotExist, ValidationError):

            # request.session['is_autenticated']= True
            #  utilisateur_id = request.session['utilisateur_id']
            #  utilisateur = Utilisateur.objects.get(id=utilisateur_id);

                return render(request,'crazymix/compte.html', {'title':'Mon compte', 'utilisateur':utilisateur,'image_src':image_src})
            else:
                return HttpResponse('Veuillez vous connecter')


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
            utilisateur=Utilisateur.objects.filter(username=username).first()

            # user = authenticate(request, username=username, password=password)
            # si la liste n'est pas vide donc il a trouvé un user avec le username et le pwd'
            if utilisateur is None:

                return redirect('login')
                # return render(request, 'registration/login.html', {'form': form})
            else:

                if check_password(password, utilisateur.password):

                    request.session['utilisateur_id'] = utilisateur.id
                    request.session['is_authenticated'] = True

                    return redirect('compte')
    else:
        # user=User(username='admin',password= make_password('12345qwe!'))
        # user.save()
        form = LoginForm()
    context={'user':request.session.get('user',None)}
    return render(request, 'registration/login.html', {'form': form,'context':context})

def register(request):
    if(request.method=="POST"):
        form = RegisterForm(request.POST,request.FILES)

        if form.is_valid():
            username=form.cleaned_data['username']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            telephone=form.cleaned_data['telephone']
            email = form.cleaned_data['email']
            adresse = form.cleaned_data['adresse']
            code_postal = form.cleaned_data['code_postal']
            spotify = form.cleaned_data['spotify']
            instagram = form.cleaned_data['instagram']
            description = form.cleaned_data['description']
            avatar = form.cleaned_data['avatar']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']
            pwd=password
            hashed_password = make_password(pwd)
            utilisateur=Utilisateur(username=username,first_name=first_name,last_name=last_name,telephone=telephone,email=email,adresse=adresse,code_postal=code_postal,spotify=spotify,instagram=instagram,
                                    description=description,avatar=avatar,role=role,password=hashed_password)
            util=Utilisateur.objects.filter(username=username)
            if len(util) ==0 :
                utilisateur.save()
                return redirect('login')
            else:
                messages.add_message(request, messages.INFO, "Ce nom d'utilisateur existe déja, Veuillez utiliser un autre")
        return render(request, 'registration/signup.html', {'form': form})
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})



# def sessionUser(request):
#     user_id=request.session.get('user_id')
#     if user_id is not None:
#         user = User.objects.get(pk=user_id)
#     else:
#         return redirect ('login')



def upload(request):
    if request.method=="POST" and request.FILES["upload"]:
        upload = request.FILES["upload"]
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request,'crazymix/upload.html',{'file_url':file_url})
    return render(request,'crazymix/upload.html')


def modifierProfil(request,id:str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method=='POST':
        idUser=request.POST.get('id')
        # form = ModifierProfilForm(request.POST, request.FILES,instance=None)


        # idUser= form.cleaned_data['id']
        utilisateur = Utilisateur.objects.get(id=idUser)

        utilisateur.last_name =request.POST.get('last_name')
        utilisateur.first_name = request.POST.get('first_name')
        utilisateur.email = request.POST.get('email')
        utilisateur.adresse = request.POST.get('adresse')
        utilisateur.code_postal =request.POST.get('code_postal')
        utilisateur.telephone =request.POST.get('telephone')
        utilisateur.avatar = request.FILES.get('avatar')
        utilisateur.spotify = request.POST.get('spotify')
        utilisateur.instagram =request.POST.get('instagram')
        utilisateur.description =request.POST.get('description')
        utilisateur.role =request.POST.get('role')

        # if form.is_valid():

        # form = ModifierProfilForm(request.POST, instance=utilisateur)

        #     form.save()
        utilisateur.save()
        # messages.success(request, 'Votre profil a été modifié avec succès.')

        return redirect ('compte')
    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form=ModifierProfilForm(instance=utilisateur)
        return render (request, 'crazymix/modifierProfil.html',{'form':form})


def modifierContact(request,id:str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method=='POST':
        idUser=request.POST.get('id')
        utilisateur = Utilisateur.objects.get(id=idUser)
        utilisateur.email = request.POST.get('email')
        utilisateur.telephone = request.POST.get('telephone')
        utilisateur.spotify = request.POST.get('spotify')
        utilisateur.instagram = request.POST.get('instagram')
        utilisateur.save()
        # messages.success(request, 'Votre profil a été modifié avec succès.')
        return redirect('compte')
    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form = ModifierContactForm(instance=utilisateur)
        return render(request, 'crazymix/modifierInfoPerso.html', {'form': form})


def modifierInfoPerso(request,id:str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method=='POST':
        idUser=request.POST.get('id')
        utilisateur = Utilisateur.objects.get(id=idUser)
        if request.FILES.get('avatar') is not None:
            utilisateur.avatar = request.FILES.get('avatar')
        utilisateur.last_name =request.POST.get('last_name')
        utilisateur.first_name = request.POST.get('first_name')
        utilisateur.save()
        # messages.success(request, 'Votre profil a été modifié avec succès.')
        return redirect('compte')
    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form = ModifierInfoPersoForm(instance=utilisateur)
        return render(request, 'crazymix/modifierContact.html', {'form': form})



def modifierAdresse(request,id:str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method=='POST':
        idUser=request.POST.get('id')
        utilisateur = Utilisateur.objects.get(id=idUser)
        utilisateur.adresse = request.POST.get('adresse')
        utilisateur.code_postal = request.POST.get('code_postal')
        utilisateur.description = request.POST.get('description')
        utilisateur.role = request.POST.get('role')
        utilisateur.save()
        # messages.success(request, 'Votre profil a été modifié avec succès.')
        return redirect('compte')
    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form = ModifierAdresseForm(instance=utilisateur)
        return render(request, 'crazymix/modifierContact.html', {'form': form})


def modifierMDP(request,id:str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method == 'POST':
        idUser = request.POST.get('id')
        utilisateur = Utilisateur.objects.get(id=idUser)
        password = request.POST.get('ancienMdp')

        ancienMdp=utilisateur.password
        nouveaumotpasse=request.POST.get('nouveaumotpasse')
        confirmatioMdp=request.POST.get('confirmatioMdp')
        if check_password(password,ancienMdp):
            if (nouveaumotpasse==confirmatioMdp):
                utilisateur.password = make_password(nouveaumotpasse)
        utilisateur.save()
        # messages.success(request, 'Votre profil a été modifié avec succès.')
        return redirect('compte')
    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form = ModifierMdpForm(instance=utilisateur)
        return render(request, 'crazymix/modifierMDP.html', {'form': form})