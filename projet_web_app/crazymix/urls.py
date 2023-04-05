from django.urls import path
from . import views
# from .views import AjaxHandler

urlpatterns = [
    path('', views.index, name='index'),
    # path('reservation/new', AjaxHandler.as_view()),
    path('reservation/new', views.reservation, name="reservation"),
    path('reservation/<reservation_id>', views.reservation, name="reservationModif"),
    path('modifierPartage/<extrait_id>', views.modifierPartage, name="modifierPartage"),
    path('changerPartage/', views.changerPartage, name="changerPartage"),
    path('valider_username/', views.valider_username, name="valider_username"),
    path('sessions/', views.sessions, name="sessions"),
    path('extraits_artistes/', views.extraits_artistes, name="extraits_artistes"),
    path('connexion/', views.connexion, name="connexion"),
    path('deconnexion/', views.deconnexion, name="deconnexion"),
    path('inscription/new', views.inscription, name="inscription"),
    path('compte/', views.compte, name="compte"),
    path('infos/', views.infos, name="infos"),
    path("upload/", views.upload, name="upload"),
    path("uploadAudio/", views.uploadAudio, name="uploadAudio"),
    path("modifierProfil/<str:id>", views.modifierProfil, name="modifierProfil"),
    path("modifierInfoPerso/<str:id>", views.modifierInfoPerso, name="modifierInfoPerso"),
    path("modifierContact/<str:id>", views.modifierContact, name="modifierContact"),
    path("modifierAdresse/<str:id>", views.modifierAdresse, name="modifierAdresse"),
    path("modifierMDP/<str:id>", views.modifierMDP, name="modifierMDP"),
    path("annulerReservation/<reservation_id>",views.annulerReservation,name="annulerReservation"),
    path("validerReservation/<reservation_id>",views.validerReservation,name="validerReservation"),
    path("supprimerExtrait/<id>", views.supprimerExtrait, name="supprimerExtrait"),
    path("validersessions/", views.validersessions, name="validersessions")
]