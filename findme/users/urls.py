from django.urls import path,include
from users import views

urlpatterns = [
    path('email', views.EamilRedundantCheck),
    path('<int:id>/', views.UserInfo.as_view(),name="user_info"),
    path('selfinfos/', views.UserInfo.as_view(),name="user_info"),
    path('', views.getUserListsByUserType),
    path('type/', views.getEachUserType.as_view(), name="get_each_user_type"),
    path('reset/password/', views.PasswordReset.as_view(), name="PasswordReset"),
    path('activate/<str:uidb64>/<str:token>',views.Activate.as_view(), name="activate")
]