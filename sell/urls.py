from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from rest_framework_jwt.views import ObtainJSONWebToken, refresh_jwt_token, verify_jwt_token

from sell_api.serializers import CustomJWTSerializer
from sell_api import views
from sell_api.views import UserCreateView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
                  path('api-token-auth/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),
                  path('api-token-refresh/', refresh_jwt_token),
                  path('api-token-verify/', verify_jwt_token),
                  path('user/login/', views.user_login, name='user_login'),
                  path('user/logout/', views.user_logout, name='user_logout'),
                  path('user/create/', UserCreateView.as_view(), name='register'),
                  path('', include('sell_api.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
