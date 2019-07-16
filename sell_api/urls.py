from django.urls import path

from sell_api.views import ItemSingleViews, UserListView, CategoryViews, ItemCreate, item_list
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Sell API')

urlpatterns = [
    path('home/', schema_view, name='home'),
    path('category/', CategoryViews.as_view()),
    path('items/', item_list),
    path('item/<int:pk>/', ItemSingleViews.as_view(), name='item_detail'),
    path('item/create/', ItemCreate.as_view()),
    path('users/', UserListView.as_view(), name='UserListView'),

]
