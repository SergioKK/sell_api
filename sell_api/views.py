from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from hitcount.views import HitCountDetailView

from sell_api.models import Category, Items, Users
from sell_api.serializers import CategorySerializer, UserSerializer, ItemSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination settings
    """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class CategoryViews(generics.ListAPIView):
    """
    View list of categories
    """
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination


class ItemListViews(generics.ListAPIView):
    """
    View list of items
    """
    permission_classes = (AllowAny,)
    serializer_class = ItemSerializer
    queryset = Items.objects.all().order_by('price', 'time_added')
    pagination_class = StandardResultsSetPagination


class ItemSingleViews(generics.RetrieveAPIView):
    """
    View item by 'id"
    """
    permission_classes = (AllowAny,)
    serializer_class = ItemSerializer
    queryset = Items.objects.all()
    pagination_class = StandardResultsSetPagination


class ItemCountHit(HitCountDetailView, ItemSingleViews):
    """
    Hit counter
    """
    model = Items
    count_hit = True
    template_name = 'items_detail.html'


class ItemCreate(generics.ListCreateAPIView):
    """
    Add item
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
    queryset = Items.objects.all()


class UserCreateView(generics.CreateAPIView):
    """
    Create user
    """
    permission_classes = (AllowAny,)
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer,)
    template_name = 'login.html'

    def get(self, request):
        queryset = Users.objects.all()
        return Response({'user': queryset}, template_name='register.html')


class UserListView(generics.ListAPIView):
    """
    View list of users
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


def test(request):
    return render(request, 'categories_and_items.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


def item_count(request):
    categories = Category.objects.all().annotate(item_count=Count('Category'))
    return render(request, 'items_in_categories.html', {'categories': categories})
