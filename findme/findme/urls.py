from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from allauth.account.views import confirm_email
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

schema_url_v1_patterns = [
    url(r'', include(('diary.urls', 'diary'), namespace='diary')),
    url(r'', include(('users.urls','users'), namespace='email')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="FINDME API",
      default_version='v1',
      description =
      '''
      **2020 SW캡스톤디자인 real kk팀 - Find Me 백엔드 API입니다.**

      - API BASE URL : http://ec2-13-209-32-113.ap-northeast-2.compute.amazonaws.com:8000/
      ''',
      contact=openapi.Contact(email="capstone4824@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['flex'],#, 'ssv'],
   public=True,
   permission_classes=(AllowAny,),
   patterns=schema_url_v1_patterns,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email,
        name='account_confirm_email'),
    path('users/', include('users.urls')),
    path('', include('diary.urls')),

    # API document generation with  drf_yasg
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/',  schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
