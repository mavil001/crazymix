from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from crazymix.models import Utilisateur, Reservation, ExtraitAudio, Favoris, Reaction
from .forms import LoginForm, RegisterForm, ModifierProfilForm, \
    ModifierInfoPersoForm, ModifierContactForm, ModifierAdresseForm, \
    ModifierMdpForm
import datetime
import base64
import calendar
from datetime import date
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from pydub import AudioSegment
from django_mongoengine.mongo_auth.managers import UserManager
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.views.generic import View
from django.http import JsonResponse
import json
from .models import STATUT
from django.db.models import Q


# Create your views here.

def index(request):
    extraits_public = ExtraitAudio.objects.all()
    user = getUser(request)
    print(extraits_public)
    extraits_liste = []
    reactionActiveBD=[]
    for x in extraits_public:

        audio_proxy = x.audio
        if audio_proxy:
            audio_bytes = audio_proxy.read()
            audio_data = base64.b64encode(audio_bytes).decode('utf-8')
            audio_src = f"data:audio/mpeg;base64,{audio_data}"
        else:
            audio_src = None

        reactionActive = None
        favori = 'False'
        if (user):
            favorisBD = Favoris.objects.filter(audio=x, utilisateur=user.id)
            if (favorisBD):
                favori = 'True'
            reactionActiveBD = Reaction.objects.filter(audio=x, utilisateur=user.id)
            if (reactionActiveBD):
                reactionActive = reactionActiveBD[0].reaction
            else:
                reactionActive = None
        reactions_liste = []
        reaction_cool = []
        reaction_frowning = []
        reaction_love = []
        reaction_winky = []
        reaction_blushing = []
        reaction_cool = getReactionList(x, 'COOL')
        reaction_frowning=getReactionList(x, 'FROWNING')
        reaction_love=getReactionList(x, 'LOVE')
        reaction_winky=getReactionList(x, 'WINKY')
        reaction_blushing=getReactionList(x, 'BLUSHING')
        reactionsBD = []
        reactionsSurplus=[]
        utilisateurs_liste=[]
        if(len(reaction_cool)!=0):
            reactionsBD.append(reaction_cool)
        if (len(reaction_frowning) != 0):
            reactionsBD.append(reaction_frowning)
        if (len(reaction_love) != 0):
            reactionsBD.append(reaction_love)
        if (len(reaction_winky) != 0):
            reactionsBD.append(reaction_winky)
        if (len(reaction_blushing) != 0):
            reactionsBD.append(reaction_blushing)
        utilisateurs_surplus=[]
        if (len(reactionsBD)!=0):
            for reactionType in reactionsBD:
                reactionSrc=""
                counter=0
                for reaction in reactionType:
                    if(len(reactionActiveBD) ==0 or len(reactionActiveBD) !=0 and reaction.id != reactionActiveBD[0].id):
                            reaction_name = reaction.reaction.lower()
                            reactionSrc = "/static/crazymix/img/{}.png".format(reaction_name)
                            image_proxy = reaction.utilisateur.avatar
                            image_bytes = image_proxy.read()
                            image_data = base64.b64encode(image_bytes).decode('utf-8')
                            image_src = f"data:image/jpeg;base64,{image_data}"
                            if(counter<=4):
                                utilisateurs_liste.append({'utilisateurImg': image_src})
                                counter+=1
                            else:
                                utilisateurs_surplus.append({'utilisateurImg':image_src, 'reaction':reactionSrc})

                if(len(utilisateurs_liste)!=0):
                    reactions_liste.append({'src': reactionSrc, 'utilisateurs_liste': utilisateurs_liste})
                    utilisateurs_liste = []
        if(utilisateurs_surplus==[]):
            utilisateurs_surplus=""
        extraits_liste.append({'audio': audio_src, 'id': x.id, 'partage': x.partage, 'nom': x.nom,
                               'favoris': favori, 'reactions': reactions_liste, 'reactionActive': reactionActive, 'utilisateurs_surplus':utilisateurs_surplus})

    return render(request, 'crazymix/index.html', {'title': 'Extraits disponibles',
                                                   'extraits_public': extraits_liste})


# return render(request, 'crazymix/index.html', {'title': 'CrazyMix - Studio'})

def bookSession(request, reservation_id=None):
    user = getUser(request)
    if (True):
        if (user != ""):
            data = request.POST
            if (data['direction'] != ""):
                return redirect('reservation')
            else:
                data = data['reservation'].strip()
                dateHeures = data.split("de")
                date = dateHeures[0].split('/')
                heureDebutFin = dateHeures[1].split("-")
                debut = heureDebutFin[0].split(':')
                fin = heureDebutFin[1].split(':')
                dateTimeDebut = datetime(int(date[2].strip()), int(date[1].strip()), int(date[0].strip()),
                                         int(debut[0].strip()), int(debut[1].strip()), 0)
                dateTimeFin = datetime(int(date[2].strip()), int(date[1].strip()), int(date[0].strip()),
                                       int(fin[0].strip()), int(fin[1].strip()), 0)

                if (validateReservation(dateTimeDebut, dateTimeFin)):
                    if (reservation_id == 'None'):
                        reservation = Reservation(debut=dateTimeDebut, fin=dateTimeFin, user=user, statut="EN_ATTENTE")
                        reservation.save()
                    else:
                        reservation = Reservation.objects.get(id=reservation_id)
                        reservation.debut = dateTimeDebut
                        reservation.fin = dateTimeFin
                        reservation.save()
                    return True
    return False


def reservation(request, reservation_id=None):
    user = getUser(request)
    if (user == ""):
        return redirect('login')
    isThisWeek = True
    if (request.method == 'POST'):

        data = request.POST
        reservation_id = request.POST.get('reservation_id')
        if (data['direction'] == ""):
            saved = bookSession(request, reservation_id)
            if (saved):
                messages.add_message(request, messages.INFO, "Réservation effectuée avec succès")
                return redirect('sessions')
            messages.add_message(request, messages.INFO, "Cette plage est déjà réservée")
            return redirect('reservation')
        else:
            dateNow = None
            today = None
            heureActuelle = 0
            cal = calendar.Calendar(firstweekday=0)
            dateBase = data['dateIndicator'].split('/')
            actualMonthDates = cal.monthdays2calendar(int(dateBase[2]), int(dateBase[1]))
            if (data['direction'] == 'previous'):
                if (dateBase[0] == "0"):
                    if (dateBase[1] == "1"):
                        newMonth = 12
                        newYear = int(dateBase[2]) - 1
                    else:
                        newMonth = int(dateBase[1]) - 1
                        newYear = int(dateBase[2])

                    monthDates = cal.monthdays2calendar(newYear, newMonth)
                    if actualMonthDates[0][0][0] == 0:
                        newMonth = int(dateBase[1]) - 1
                        newYear = int(dateBase[2])
                        index_semaine = len(monthDates) - 2

                    index_semaine = len(monthDates) - 1
                else:
                    if dateBase[0] == '1' and actualMonthDates[0][0][0] == 0:
                        newMonth = int(dateBase[1]) - 1
                        newYear = int(dateBase[2])
                        monthDates = cal.monthdays2calendar(newYear, newMonth)
                        index_semaine = len(monthDates) - 1
                    else:
                        newMonth = int(dateBase[1])
                        newYear = int(dateBase[2])
                        index_semaine = int(dateBase[0]) - 1
                        monthDates = cal.monthdays2calendar(newYear, newMonth)

            elif (data['direction'] == 'next'):
                if (len(actualMonthDates) - 1 == int(dateBase[0])):
                    # si derniere semaine du mois et que dates semaine finissent par 0 aloors ajouter une semaine d eplus

                    if (int(dateBase[1]) == 12):
                        newMonth = 1
                        newYear = int(dateBase[2]) + 1
                        newWeek = 0
                    else:
                        newWeek = 0
                        newMonth = int(dateBase[1]) + 1
                        newYear = int(dateBase[2])
                    if actualMonthDates[len(actualMonthDates) - 1][6][0] == 0:
                        index_semaine = 1
                    else:
                        index_semaine = 0
                    monthDates = cal.monthdays2calendar(newYear, newMonth)
                else:
                    newMonth = int(dateBase[1])
                    newYear = int(dateBase[2])
                    index_semaine = int(dateBase[0]) + 1
                    monthDates = cal.monthdays2calendar(newYear, newMonth)
            dateRef = date(newYear, newMonth, 1)
            dateNow = datetime.now()
            if (data['dateToday'] != 'None'):
                dateToday = data['dateToday'].split(':')
                splitedInfos = []
                splitedInfos.append(dateToday[1].split(','))
                splitedInfos.append(dateToday[2].split(','))
                splitedInfos.append(dateToday[3].split(','))
                splitedInfos.append(dateToday[4].split('}'))
                dateTodayCleaned = {'date': int(splitedInfos[0][0].strip()), 'week': int(splitedInfos[1][0].strip()),
                                    'month': int(splitedInfos[2][0].strip()), 'year': int(splitedInfos[3][0].strip())}
                today = dateTodayCleaned
                if dateRef.year == int(dateTodayCleaned['year']) and dateRef.month == int(
                        dateTodayCleaned['month']) and index_semaine == int(dateTodayCleaned['week']):
                    isThisWeek = "True"
                    return redirect('reservation')
                else:
                    isThisWeek = None
            else:
                isThisWeek = None
    else:
        data = None
        # Date aujourd'hui
        dateNow = datetime.now()
        today = dateNow.day
        heureActuelle = dateNow.hour
        cal = calendar.Calendar(firstweekday=0)
        monthDates = cal.monthdays2calendar(dateNow.year, dateNow.month)

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
        today = {'date': dateNow.day, 'week': index_semaine, 'month': dateNow.month, 'year': dateNow.year}
        dateRef = dateNow

    # Render calendrier
    # Texte
    joursSemaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
            "Novembre",
            "Décembre"]
    heures = []
    for h in range(8, 20):
        classe = None
        if (dateNow is not None and h <= dateNow.hour):
            classe = 'text-secondary px-2'

        heures.append({'hDebut': h, 'hFin': h + 1, 'classe': classe})

    # Indicateur semaine/mois/année
    dateIndicator = "{}/{}/{}".format(index_semaine, dateRef.month, dateRef.year)
    # Recherche des données du mois précédent si se chevauchent
    semainePadding = []
    previousMonthIncluded = False
    nextMonthIncluded = False
    if index_semaine == 0 and monthDates[index_semaine][0][0] == 0:
        previousMonthIncluded = True
        previousMonth = 0
        previousYear = dateRef.year
        if dateRef.month == 1:
            previousYear = dateRef.year - 1
            previousMonth = 12
        else:
            previousMonth = dateRef.month - 1
        paddingMonthDates = cal.monthdays2calendar(previousYear, previousMonth)
        semainePadding = paddingMonthDates[len(paddingMonthDates) - 1]
    elif index_semaine == len(monthDates) - 1 and monthDates[index_semaine][
        len(monthDates[index_semaine]) - 1][0] == 0:
        nextMonthIncluded = True
        nextYear = dateRef.year
        if dateRef.month == 12:
            nextYear = dateRef.year + 1
            nextMonth = 1
        else:
            nextMonth = dateRef.month + 1

        paddingMonthDates = cal.monthdays2calendar(nextYear, nextMonth)
        semainePadding = paddingMonthDates[0]

    # Stockage des dates de la semaine incluant les chevauchements
    semaineActuelle = monthDates[index_semaine]
    datesSemaine = []
    for index in range(7):
        classe = None
        style = None
        if semaineActuelle[index][0] == 0:
            if previousMonthIncluded and isThisWeek is not None:
                classe = 'text-secondary px-2'
                month = previousMonth
                year = previousYear
            elif nextMonthIncluded:
                month = nextMonth
                year = nextYear
            else:
                month = dateRef.month
                year = dateRef.year
            datesSemaine.append(
                {'dateComplete': "{}/{}/{}".format(semainePadding[index][0], month, year),
                 'jour': joursSemaine[index],
                 'classe': classe, 'style': style, 'date': semainePadding[index][0],
                 'year': year, 'month': month, 'indisponibilites': []})

        else:
            if request.method == 'GET' and semaineActuelle[index][0] == today['date']:
                style = "background-color: #5a6268;border-radius:7px;"
            elif ((request.method == 'GET' and semaineActuelle[index][0] < today['date'])):
                classe = 'text-secondary px-2'
            datesSemaine.append(
                {'dateComplete': "{}/{}/{}".format(semaineActuelle[index][0], dateRef.month, dateRef.year),
                 'date': semaineActuelle[index][0], 'jour': joursSemaine[index],
                 'classe': classe, 'style': style, 'month': dateRef.month, 'year': dateRef.year,
                 'indisponibilites': []})

    firstDate = datetime(datesSemaine[0]['year'], datesSemaine[0]['month'], datesSemaine[0]['date'], 0, 0, 0)
    lastIndex = len(datesSemaine) - 1
    lastDate = datetime(datesSemaine[lastIndex]['year'], datesSemaine[lastIndex]['month'],
                        datesSemaine[lastIndex]['date'], 23, 59, 59)
    reservations = Reservation.objects.filter(debut__gte=firstDate, fin__lte=lastDate)

    if (len(reservations) != 0):
        for reservation in reservations:
            for jour in datesSemaine:
                indisponibilites = []
                if reservation['debut'].day == jour['date']:
                    for i in range(reservation['debut'].hour, reservation['fin'].hour):
                        jour['indisponibilites'].append(i)

    # Attribution du/des nom(s) de(s) mois de la semaine
    moisSemaine = mois[dateRef.month - 1]
    if previousMonthIncluded:
        moisSemaine = "{0} / {1}".format(mois[previousMonth - 1], moisSemaine)
    elif nextMonthIncluded:
        moisSemaine = "{0} / {1}".format(moisSemaine, mois[nextMonth - 1])

    return render(request, 'crazymix/reservation.html', {'title': "Réserver une session d'enregistrement",
                                                         'jours_semaine': joursSemaine,
                                                         'datesSemaine': datesSemaine,
                                                         'moisSemaine': moisSemaine, 'today': today,
                                                         "heureActuelle": heureActuelle, 'heures': heures,
                                                         "dateIndicator": dateIndicator, 'isThisWeek': isThisWeek,
                                                         "year": dateRef.year, 'reservation_id': reservation_id})


def sessions(request):
    utilisateur_id = request.session['utilisateur_id']
    user = Utilisateur.objects.get(id=utilisateur_id)
    reservations = Reservation.objects.filter(user=utilisateur_id)
    if (len(reservations) == 0):
        reservations = None
    return render(request, 'crazymix/sessions.html',
                  {'title': "Mes sessions d'enregistrement", "reservations": reservations, 'user': user})


def validersessions(request):
    utilisateur_id = request.session['utilisateur_id']
    user = Utilisateur.objects.get(id=utilisateur_id)
    if (user.role == "PROFESSIONNEL"):
        reservations = Reservation.objects.filter(statut="EN_ATTENTE")
        if (len(reservations) == 0):
            reservations = None
        return render(request, 'crazymix/validerSessions.html',
                      {'title': "Validation de sessions", "reservations": reservations, 'user': user})
    else:
        return redirect("index")


def extraits_artistes(request):
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        utilisateur_id = request.session['utilisateur_id']
        extraits = ExtraitAudio.objects.filter(utilisateur=utilisateur_id)

        extrait = None
        partage = 'PUBLIC'
        if (request.method == "POST"):
            audio = request.FILES.get('uploadAudio')
            utilisateur_id = request.session['utilisateur_id']
            utilisateur = Utilisateur.objects.get(id=utilisateur_id)
            nom = request.POST.get('nom')
            public = request.POST.get('public')
            communaute = request.POST.get('communaute')
            personnel = request.POST.get('personnel')
            partage = request.POST.get('partage')
            if partage == 'PUBLIC':
                extrait = ExtraitAudio(audio=audio, utilisateur=utilisateur, partage='PUBLIC', nom=nom)
            elif partage == 'COMMUNAUTE':
                extrait = ExtraitAudio(audio=audio, utilisateur=utilisateur, partage='COMMUNAUTE', nom=nom)
            elif partage == 'PERSONNEL':
                extrait = ExtraitAudio(audio=audio, utilisateur=utilisateur, partage='PERSONNEL', nom=nom)
            extrait.save()
            return redirect('extraits_artistes')
        extraits_liste = []
        for x in extraits:

            audio_proxy = x.audio
            if audio_proxy:
                audio_bytes = audio_proxy.read()
                audio_data = base64.b64encode(audio_bytes).decode('utf-8')
                audio_src = f"data:audio/mpeg;base64,{audio_data}"
            else:
                audio_src = None
            extraits_liste.append({'audio': audio_src, 'id': x.id, 'partage': x.partage, 'nom': x.nom})

        return render(request, 'crazymix/extraits_artistes.html',
                      {'title': 'Mes extraits', 'extraits': extraits_liste, 'utilisateur_id': utilisateur_id})
    else:
        return redirect('login')


def modifierFavoris(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        extrait_id = data['extrait_id']
        favoris = data['favoris']
        extrait = ExtraitAudio.objects.get(id=extrait_id)
        if extrait:
            user = getUser(request)
            if user:
                favorisBD = Favoris.objects.filter(utilisateur=user.id, audio=extrait)
                if (favoris == 'False' and not favorisBD):
                    favorisCree = Favoris(utilisateur=user.id, audio=extrait)
                    favorisCree.save()
                elif (favoris == 'True' and favorisBD):
                    favorisBD.delete()
        return JsonResponse({'valid': 'valid', 'favoris': favoris, 'extrait_id': extrait_id})
    return JsonResponse({'valid': 'invalid'})


def modifierReaction(request):
    valid = 'invalid'
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        extrait_id = data['extrait_id']
        reaction = data['reaction']
        extrait = ExtraitAudio.objects.get(id=extrait_id)
        if extrait:
            user = getUser(request)
            if user:
                valid = 'valid'
                reactionBD = Reaction.objects.filter(utilisateur=user.id, audio=extrait)
                if (not reactionBD):
                    ReactionCree = Reaction(utilisateur=user.id, audio=extrait, reaction=reaction)
                    ReactionCree.save()
                else:
                    laReaction = Reaction.objects.get(id=reactionBD[0].id)
                    if (laReaction.reaction != reaction):
                        laReaction.reaction = reaction
                        laReaction.save()
                    else:
                        valid = 'invalid'
                        laReaction.delete()
        return JsonResponse({'valid': valid, 'reaction': reaction, 'extrait_id': extrait_id})
    return JsonResponse({'valid': valid})


def changerPartage(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        extrait_id = data['extrait_id']
        extrait = ExtraitAudio.objects.get(id=extrait_id)
        partage = extrait.partage
        if (extrait.partage == 'PUBLIC'):
            extrait.partage = 'COMMUNAUTE'
        elif (extrait.partage == 'COMMUNAUTE'):
            extrait.partage = 'PERSONNEL'
        elif (extrait.partage == 'PERSONNEL'):
            extrait.partage = 'PUBLIC'
        extrait.save()
        return JsonResponse({'valid': 'valid', 'partage': partage, 'extrait_id': extrait_id})
    return JsonResponse({'valid': 'invalid'})


# def modifierPartage(request, extrait_id : str):
#     extrait = ExtraitAudio.objects.get(id=extrait_id)
#     if(extrait.partage=='PUBLIC'):
#         extrait.partage='COMMUNAUTE'
#     elif(extrait.partage=='COMMUNAUTE'):
#         extrait.partage='PERSONNEL'
#     elif(extrait.partage=='PERSONNEL'):
#         extrait.partage='PUBLIC'
#
#     if request.POST.get('public'):
#         extrait.partage='PUBLIC'
#     elif request.POST.get('communaute'):
#         extrait.partage = 'COMMUNAUTE'
#     elif request.POST.get('personnel'):
#         extrait.partage = 'Pesonnel'
#     extrait.save()
#     return redirect('extraits_artistes')

def connexion(request):
    return render(request, 'crazymix/connexion.html', {'title': 'Se connecter'})


def deconnexion(request):
    request.session.clear()
    return redirect('index')


def inscription(request):
    # form = UserForm()
    return render(request, 'registration/signup.html', {'title': "S'inscrire"})
    # return render(request,'crazymix/inscription.html', {'title':"S'inscrire", 'form' : form})


def compte(request):
    # def authenticate(self, username=None, password=None, **kwargs):
    #     try:
    ab = request.session.get('is_authenticated')

    if 'is_authenticated' in request.session and request.session['is_authenticated']:

        utilisateur_id = request.session['utilisateur_id']
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        image_proxy = utilisateur.avatar
        image_bytes = image_proxy.read()
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        image_src = f"data:image/jpeg;base64,{image_data}"

        # except (DoesNotExist, ValidationError):

        # request.session['is_autenticated']= True
        #  utilisateur_id = request.session['utilisateur_id']
        #  utilisateur = Utilisateur.objects.get(id=utilisateur_id);

        return render(request, 'crazymix/compte.html',
                      {'title': 'Mon compte', 'utilisateur': utilisateur, 'image_src': image_src})
    else:
        return HttpResponse('Veuillez vous connecter')


def infos(request):
    return render(request, 'crazymix/infos.html', {'title': 'Informations sur le site du studio'})


def valider_username(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        username = data['username']
        utilisateur = Utilisateur.objects.filter(username=username).first()
        if utilisateur is None:
            return JsonResponse({'valid': 'invalid'})
        return JsonResponse({'valid': 'valid'})


def login(request):
    if (request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # pwd=password
            # hashed_password = make_password(pwd)
            # if check_password('password', hashed_password):
            utilisateur = Utilisateur.objects.filter(username=username).first()

            # user = authenticate(request, username=username, password=password)
            # si la liste n'est pas vide donc il a trouvé un user avec le username et le pwd'
            if utilisateur is None:
                messages.add_message(request, messages.INFO,
                                     "Le nom d'utilisateur et/ou le mot de passe n'est pas valide")

                form.password = ""
                # return redirect('login')
                # return render(request, 'registration/login.html', {'form': form})
            else:

                if check_password(password, utilisateur.password):
                    request.session['utilisateur_id'] = utilisateur.id
                    request.session['is_authenticated'] = True
                    if utilisateur.role == 'PROFESSIONNEL':
                        request.session['professionnel'] = True
                    return redirect('compte')
                else:
                    messages.add_message(request, messages.INFO,
                                         "Le nom d'utilisateur et/ou le mot de passe n'est pas valide")

                    form.password = ""
    else:
        # user=User(username='admin',password= make_password('12345qwe!'))
        # user.save()
        form = LoginForm()
    context = {'user': request.session.get('user', None)}
    return render(request, 'registration/login.html', {'form': form, 'context': context})


def register(request):
    if (request.method == "POST"):
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            telephone = form.cleaned_data['telephone']
            email = form.cleaned_data['email']
            adresse = form.cleaned_data['adresse']
            code_postal = form.cleaned_data['code_postal']
            spotify = form.cleaned_data['spotify']
            instagram = form.cleaned_data['instagram']
            description = form.cleaned_data['description']
            avatar = form.cleaned_data['avatar']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']
            pwd = password
            hashed_password = make_password(pwd)
            utilisateur = Utilisateur(username=username, first_name=first_name, last_name=last_name,
                                      telephone=telephone, email=email, adresse=adresse, code_postal=code_postal,
                                      spotify=spotify, instagram=instagram,
                                      description=description, avatar=avatar, role=role, password=hashed_password)
            util = Utilisateur.objects.filter(username=username)
            if len(util) == 0:
                utilisateur.save()
                return redirect('login')
            else:
                messages.add_message(request, messages.INFO,
                                     "Ce nom d'utilisateur existe déja, Veuillez utiliser un autre")
        return render(request, 'registration/signup.html', {'form': form})
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def upload(request):
    if request.method == "POST" and request.FILES["upload"]:
        upload = request.FILES["upload"]
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request, 'crazymix/upload.html', {'file_url': file_url})
    return render(request, 'crazymix/upload.html')


def uploadAudio(request):
    if request.method == "POST" and request.FILES["upload"]:
        audio_file = request.FILES["upload"]

        # audio=AudioSegment.from_file(audio_file)
        # extract = audio[2 * 60 * 1000: 2 * 60 * 1000 + 30 * 1000]
        fss = FileSystemStorage()
        file = fss.save(audio_file.name, audio_file)
        # récupérer l'URL du fichier extrait
        file_url = fss.url(file)

        return render(request, "crazymix/uploadAudio.html", {"file_url": file_url})
    return render(request, "crazymix/uploadAudio.html")


def getUser(request):
    utilisateur = ""
    if 'is_authenticated' in request.session and request.session['is_authenticated']:
        utilisateur_id = request.session['utilisateur_id']
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
    return utilisateur


def getReactionList(audio, reaction):
    reactionsBD = Reaction.objects.filter(audio=audio, reaction=reaction)

    return reactionsBD


def validateReservation(dateTimeDebut, dateTimeFin):
    reservations = Reservation.objects(debut__lte=dateTimeFin, fin__gte=dateTimeFin)
    if (len(reservations) == 0):
        return True
    return False


def modifierProfil(request, id: str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method == 'POST':
        idUser = request.POST.get('id')
        # form = ModifierProfilForm(request.POST, request.FILES,instance=None)

        # idUser= form.cleaned_data['id']
        utilisateur = Utilisateur.objects.get(id=idUser)

        utilisateur.last_name = request.POST.get('last_name')
        utilisateur.first_name = request.POST.get('first_name')
        utilisateur.email = request.POST.get('email')
        utilisateur.adresse = request.POST.get('adresse')
        utilisateur.code_postal = request.POST.get('code_postal')
        utilisateur.telephone = request.POST.get('telephone')
        utilisateur.avatar = request.FILES.get('avatar')
        utilisateur.spotify = request.POST.get('spotify')
        utilisateur.instagram = request.POST.get('instagram')
        utilisateur.description = request.POST.get('description')
        utilisateur.role = request.POST.get('role')

        if form.is_valid() or len(form.errors) == 1:
            utilisateur.save()
            messages.add_message(request, messages.INFO, "Modification effectuée avec succès")
            return redirect('compte')
        else:
            utilisateur = Utilisateur.objects.get(id=id)
            form = ModifierProfilForm(instance=utilisateur)
        return render(request, 'crazymix/modifierProfil.html', {'form': form})


def modifierContact(request, id: str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method == 'POST':
        form = ModifierContactForm(request.POST, instance=utilisateur)
        # idUser = request.POST.get('id')
        # utilisateur = Utilisateur.objects.get(id=idUser)
        utilisateur.email = request.POST.get('email')
        utilisateur.telephone = request.POST.get('telephone')
        utilisateur.spotify = request.POST.get('spotify')
        utilisateur.instagram = request.POST.get('instagram')
        if form.is_valid() or len(form.errors) == 1:
            utilisateur.save()
            messages.add_message(request, messages.INFO, "Modification effectuée avec succès")
            return redirect('compte')
    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form = ModifierContactForm(instance=utilisateur)
    return render(request, 'crazymix/modifierInfoPerso.html', {'form': form})


def modifierInfoPerso(request, id: str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method == 'POST':
        # idUser = request.POST.get('id')
        # utilisateur = Utilisateur.objects.get(id=idUser)
        form = ModifierInfoPersoForm(request.POST, instance=utilisateur)
        if request.FILES.get('avatar') is not None:
            utilisateur.avatar = request.FILES.get('avatar')
        utilisateur.last_name = request.POST.get('last_name')
        utilisateur.first_name = request.POST.get('first_name')
        if form.is_valid() or len(form.errors) == 1:
            utilisateur.save()
            messages.add_message(request, messages.INFO, "Modification effectuée avec succès")
            return redirect('compte')
    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form = ModifierInfoPersoForm(instance=utilisateur)
    return render(request, 'crazymix/modifierContact.html', {'form': form})


def modifierAdresse(request, id: str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method == 'POST':
        form = ModifierAdresseForm(data=request.POST, instance=utilisateur)
        # idUser = request.POST.get('id')
        # utilisateur = Utilisateur.objects.get(id=idUser)
        utilisateur.adresse = request.POST.get('adresse')
        utilisateur.code_postal = request.POST.get('code_postal')
        utilisateur.description = request.POST.get('description')
        utilisateur.role = request.POST.get('role')

        if form.is_valid() or len(form.errors) == 1:
            utilisateur.save()
            messages.add_message(request, messages.INFO, "Modification effectuée avec succès")
            return redirect('compte')

    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form = ModifierAdresseForm(instance=utilisateur)
    return render(request, 'crazymix/modifierContact.html', {'form': form})


def modifierMDP(request, id: str):
    utilisateur = Utilisateur.objects.get(id=id)
    if request.method == 'POST':
        form = ModifierMdpForm(request.POST, instance=utilisateur)

        # idUser = request.POST.get('id')
        # utilisateur = Utilisateur.objects.get(id=idUser)
        password = request.POST.get('ancienMdp')

        ancienMdp = utilisateur.password
        nouveaumotpasse = request.POST.get('nouveaumotpasse')
        confirmatioMdp = request.POST.get('confirmatioMdp')
        if check_password(password, ancienMdp):
            if (nouveaumotpasse == confirmatioMdp):
                utilisateur.password = make_password(nouveaumotpasse)
        if form.is_valid() or len(form.errors) == 1:
            utilisateur.save()
            messages.add_message(request, messages.INFO, "Modification effectuée avec succès")
            return redirect('compte')
    else:
        utilisateur = Utilisateur.objects.get(id=id)
        form = ModifierMdpForm(instance=utilisateur)
    return render(request, 'crazymix/modifierMDP.html', {'form': form})


def annulerReservation(request, reservation_id):
    utilisateur_id = request.session['utilisateur_id']
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return HttpResponse("Reservation n'existe pas")
    reservation.delete()
    return redirect('sessions')


def validerReservation(request, reservation_id):
    utilisateur_id = request.session['utilisateur_id']
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return HttpResponse("Reservation n'existe pas")
    reservation.statut = 'VALIDE'
    reservation.save()
    return redirect('sessions')


def supprimerExtrait(request, id):
    utilisateur_id = request.session['utilisateur_id']
    try:
        extraits_artistes = ExtraitAudio.objects.get(id=id)
    except ExtraitAudio.DoesNotExist:
        return HttpResponse("")

    extraits_artistes.delete()
    return redirect('extraits_artistes')
