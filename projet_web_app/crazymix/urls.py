from django.urls import path
from . import views
# from .views import AjaxHandler

urlpatterns = [
    path('', views.index, name='index'),
    # path('reservation/new', AjaxHandler.as_view()),
    path('reservation/new', views.reservation, name="reservation"),
    path('sessions/', views.sessions, name="sessions"),
    path('extraits_artistes/', views.extraits_artistes, name="extraits_artistes"),
    path('connexion/', views.connexion, name="connexion"),
    path('deconnexion/', views.deconnexion, name="deconnexion"),
    path('inscription/new', views.inscription, name="inscription"),
    path('compte/', views.compte, name="compte"),
    path('infos/', views.infos, name="infos"),
    path("upload/", views.upload, name="upload"),
    path("modifierProfil/<str:id>", views.modifierProfil, name="modifierProfil"),
    path("modifierInfoPerso/<str:id>", views.modifierInfoPerso, name="modifierInfoPerso"),
    path("modifierContact/<str:id>", views.modifierContact, name="modifierContact"),
    path("modifierAdresse/<str:id>", views.modifierAdresse, name="modifierAdresse"),
    path("modifierMDP/<str:id>", views.modifierMDP, name="modifierMDP")
]