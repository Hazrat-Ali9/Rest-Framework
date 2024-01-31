from rest_framework import serializers
from .models import DataModel
from django.contrib.auth.models import User
class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataModel
        fields = '__all__'
        
        

