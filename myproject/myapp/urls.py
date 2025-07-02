from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('adduser', views.adduser),
    path('login',views.login),
    path('userhome',views.userhome),
    path('mail',views.mail),
    path('updatemail',views.updatemail),
    path('chkphish',views.chkphish),
    path('predict_ml',views.predict_ml),
    path('logout',views.login),
]
