from django.urls import path,include
from users import views

urlpatterns = [
    path('email', views.EamilRedundantCheck),
    path('', views.getUserListsByUserType),
    path('type/', views.getEachUserType.as_view(), name="get_each_user_type")
]