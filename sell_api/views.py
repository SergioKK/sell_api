from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from sell_api.models import Category, Items, Subcategory, Users
from sell_api.serializers import CategorySerializer, ItemSerializer, SubcategorySerializer, UserSerializer


from django.contrib.auth.models import User


class CategoryViews(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ItemViews(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
    queryset = Items.objects.all()


class SubcategoryViews(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.all()


class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer,)
    template_name = 'base.html'

    def get(self, request):
        queryset = Users.objects.all()
        return Response({'user': queryset}, template_name='register.html')


class UserListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


def start(request):
    return render(request, 'start.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('start'))


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
