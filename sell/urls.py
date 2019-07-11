from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import ObtainJSONWebToken

from sell_api.serializers import CustomJWTSerializer
from sell_api import views
from sell_api.views import UserCreateView

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
                  path('api-token-auth/', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)),
                  path('user_login/', views.user_login, name='user_login'),
                  path('user_logout', views.user_logout, name='user_logout'),
                  path('start/', views.start, name='start'),
                  path('user/create/', UserCreateView.as_view(), name='register'),
                  path('', include('sell_api.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
