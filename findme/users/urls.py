from django.urls import path,include
from users import views

urlpatterns = [
    path('email', views.EamilRedundantCheck),
    path('', views.getUserListsByUserType),
]