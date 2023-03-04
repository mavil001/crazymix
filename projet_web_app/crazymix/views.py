import datetime

from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, ReservationForm
from .models import User
import calendar
from datetime import date
from datetime import datetime


# Create your views here.


def index(request):
    return render(request, 'crazymix/index.html', {'title': 'CrazyMix - Studio'})


def reservation(request):
    form = ReservationForm()
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


def sessions(request):
    return render(request, 'crazymix/sessions.html', {'title': "Mes sessions d'enregistrement"})


def extraits_artistes(request):
    return render(request, 'crazymix/extraits_artistes.html', {'title': 'Exraits - Artistes'})


def connexion(request):
    return render(request, 'crazymix/connexion.html', {'title': 'Se connecter'})


def inscription(request):
    # form = UserForm()
    return render(request, 'registration/signup.html', {'title': "S'inscrire", 'form': form})
    # return render(request,'crazymix/inscription.html', {'title':"S'inscrire", 'form' : form})


def compte(request):
    return render(request, 'crazymix/compte.html', {'title': 'Mon compte'})


def infos(request):
    return render(request, 'crazymix/infos.html', {'title': 'Informations sur le site du studio'})


def login(request):
    if (request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if (request.method == "POST"):
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            id = form.cleaned_data['id']
            email = form.cleaned_data['email']
            spotify = form.cleaned_data['spotify']
            instagram = form.cleaned_data['instagram']
            description = form.cleaned_data['description']
            avatar = form.cleaned_data['avatar']
            role = form.cleaned_data['role']
            password = form.cleaned_data['passwor']

            user = User(first_name=first_name, last_name=last_name, id=id, email=email, spotify=spotify,
                        instagram=instagram, description=description, avatar=avatar, role=role, password=password, )

            user.save()
            return redirect('login')
        return render(request, 'registration/signup.html', {'form': form})
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})
