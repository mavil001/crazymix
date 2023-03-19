from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from django.http import HttpResponse
from crazymix.models import Utilisateur, Reservation
# from .forms import UserForm
from .forms import LoginForm,RegisterForm
import datetime
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
from django.views.generic import View
from django.http import JsonResponse
import json
from .models import STATUT
# Create your views here.

def index (request):
    return render(request,'crazymix/index.html', {'title':'CrazyMix - Studio'})

def render_reservation_page():
    return ""
class AjaxHandler(View):
    def post(self, request):
        user = getUser(request)
        if(True):
        # if(user != ""):
            data=json.loads(request.body)
            data=data['reservation'].strip()
            dateHeures=data.split("de")
            date=dateHeures[0].split('/')
            heureDebutFin=dateHeures[1].split("-")
            debut=heureDebutFin[0].split(':')
            fin=heureDebutFin[1].split(':')
            dateTimeDebut=datetime(int(date[2].strip()), int(date[1].strip()), int(date[0].strip()),
                                   int(debut[0].strip()), int(debut[1].strip()), 0)
            dateTimeFin= datetime(int(date[2].strip()), int(date[1].strip()), int(date[0].strip()),
                                  int(fin[0].strip()), int(fin[1].strip()), 0)

            # valid=validateReservation(dateTimeDebut, dateTimeFin)
            if(True):
                reservation=Reservation(debut=dateTimeDebut, fin=dateTimeFin, user=user, statut="EN_ATTENTE")
                reservation.save()
                # return redirect('sessions')
        #     si valide, rediriger vers la page des sessions avec message, sinon remettre formulaire avec message
        return JsonResponse({'Success':'success'})
    def get(self, request):

        # Date aujourd'hui
        dateNow = datetime.now()
        today = dateNow.day
        heureActuelle = dateNow.hour
        cal = calendar.Calendar(firstweekday=0)
        monthDates = cal.monthdays2calendar(dateNow.year, dateNow.month)

        # Texte
        joursSemaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
                "Novembre",
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
        elif index_semaine == len(monthDates) - 1 and monthDates[index_semaine][
            len(monthDates[index_semaine] - 1)] == 0:
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
                    month=previousMonth
                    year=previousYear
                elif nextMonthIncluded:
                    month=nextMonth
                    year=nextYear
                else:
                    month=dateNow.month
                    year=dateNow.year
                datesSemaine.append(
                    {'dateComplete': "{}/{}/{}".format(semainePadding[index][0], month, year), 'jour': joursSemaine[index],
                     'classe': classe, 'style': style, 'date':semainePadding[index][0],
                     'heures': heures})

            else:
                if semaineActuelle[index][0] == today:
                    style = "background-color: #5a6268;border-radius:7px;"
                elif semaineActuelle[index][0] < today:
                    classe = 'text-secondary'
                datesSemaine.append(
                    {'dateComplete': "{}/{}/{}".format(semaineActuelle[index][0], dateNow.month, dateNow.year),
                     'date':semaineActuelle[index][0], 'jour': joursSemaine[index],
                     'classe': classe, 'style': style})

        # Attribution du/des nom(s) de(s) mois de la semaine
        moisSemaine = mois[dateNow.month - 1]
        if previousMonthIncluded:
            moisSemaine = "{0} / {1}".format(mois[previousMonth - 1], moisSemaine)
        elif nextMonthIncluded:
            moisSemaine = "{0} / {1}".format(moisSemaine, mois[nextMonth - 1])

        return render(request, 'crazymix/reservation.html', {'title': "Réserver une session d'enregistrement",
                                                             'jours_semaine': joursSemaine, 'datesSemaine': datesSemaine,
                                                             'moisSemaine': moisSemaine, 'today': dateNow.day,
                                                             "heureActuelle": dateNow.hour, 'heures': heures})

        # return render(request, 'crazymix/reservation.html')

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


        # except (DoesNotExist, ValidationError):

            # request.session['is_autenticated']= True
            #  utilisateur_id = request.session['utilisateur_id']
            #  utilisateur = Utilisateur.objects.get(id=utilisateur_id);

                return render(request,'crazymix/compte.html', {'title':'Mon compte', 'utilisateur':utilisateur})
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
            email = form.cleaned_data['email']
            spotify = form.cleaned_data['spotify']
            instagram = form.cleaned_data['instagram']
            description = form.cleaned_data['description']
            avatar = form.cleaned_data['avatar']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']
            pwd=password
            hashed_password = make_password(pwd)
            utilisateur=Utilisateur(username=username,first_name=first_name,last_name=last_name,email=email,spotify=spotify,instagram=instagram,
                                    description=description,avatar=avatar,role=role,password=hashed_password)

            utilisateur.save()
            return redirect('login')
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

def getUser(request):
    utilisateur=""
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        utilisateur_id = request.session['utilisateur_id']
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
    return utilisateur

def validateReservation(dateTimeDebut, dateTimeFin):

    reservations= Reservation.objects(debut_lte=dateTimeFin, fin_gte=dateTimeFin)
    if(reservations and len(reservations)==0):
        return True
    return False
