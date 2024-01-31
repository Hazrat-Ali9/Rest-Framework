from django.shortcuts import render
from rest_framework.views import APIView
from .models import DataModel
from .serializers import DataSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from django.http import Http404
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.http import JsonResponse
import json



class DataList(APIView):
    
    def get(self, request, format=None):
        models = DataModel.objects.all()
        serializer = DataSerializer(models, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DataUpdateDelete(APIView):
   
    def get_object(self, pk):
        try:
            return DataModel.objects.get(pk=pk)
        except DataModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DataSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DataSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ProductSearchAPIView(generics.ListAPIView):
    queryset = DataModel.objects.all()
    serializer_class = DataSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({'message': 'Registration successful.'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:  # Check if the user is an admin
                return redirect('admin')  # Redirect to admin dashboard
            else:
                return redirect('home')  # Redirect to user dashboard
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')  # Redirect back to login page
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')