from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('calculadora/', views.calculadora_view, name='calculadora'),
    path('apagar_historico/', views.apagar_historico, name='apagar_historico'),
]
