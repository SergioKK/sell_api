from django.urls import path

from sell_api.views import ItemSingleViews, UserListView, CategoryViews, ItemCreate, item_list
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Sell API')

urlpatterns = [
    path('category/', CategoryViews.as_view(), name='Category view'),
    path('items/', item_list, name='List of items'),
    path('item/<int:pk>/', ItemSingleViews.as_view(), name='Detail of single item'),
    path('item/create/', ItemCreate.as_view(), name='Create new item'),
    path('users/', UserListView.as_view(), name='List of users'),

]
