from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from sell_api.views import CategoryViews, ItemViews, SubcategoryViews, UserListView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Sell API')

urlpatterns = [
    path('home/', schema_view, name='home'),
    path('category/', CategoryViews.as_view()),
    path('category/int<pk:>/', CategoryViews.as_view()),
    path('subcategory/', SubcategoryViews.as_view()),
    path('subcategory/int<pk:>/', SubcategoryViews.as_view()),
    path('item/', ItemViews.as_view()),
    path('category/int<pk:>/', ItemViews.as_view()),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('users/', UserListView.as_view(), name='UserListView'),

]
