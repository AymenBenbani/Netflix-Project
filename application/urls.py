# application/urls.py
from django.urls import path
from . import views 
 #-------------------------------aymen-------------------------


urlpatterns = [
    path('',views.index,name='app-index'),
    path('dashboard/', views.dashboard, name='app-dashboard'),  # Définissez l'URL pour dashboard
    path('mostPopular/',views.mostPopular,name='app-mostPopular'),
    path('weeklyRanking/',views.weeklyRanking,name='app-weeklyRanking'),
    path('recommenderSystem/',views.recommenderSystem,name='app-recommenderSystem'),

]

