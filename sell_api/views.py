from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from sell_api.models import Category, Item, Users
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


class ItemSingleViews(DetailView):
    """
    View and count visits of single item
    """
    model = Item
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemSingleViews, self).get_context_data(**kwargs)
        self.object.add_visit()
        self.object.save()
        return context


class ItemCreate(generics.ListCreateAPIView):
    """
    Add item
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


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
    queryset = Users.objects.all()
    serializer_class = UserSerializer


@login_required
def item_list(request):
    """
    View and order items
    """
    order_by = request.GET.get('order_by', "price")
    items = Item.objects.all().order_by(order_by)
    return render(request, 'order_by.html', {"items": items})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('/'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('/'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})
