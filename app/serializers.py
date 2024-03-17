from rest_framework import serializers
from django.contrib.auth.models import User
from .models import GroceryItem, GroceryList
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email'].split('@')[0]

        return User.objects.create_user(**validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed as e:
            username = attrs.get('username')  
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()

            if not user:
                raise AuthenticationFailed({'success': False, 'msg':'No active account found with the given credentials'})
            else:
                try:
                    attrs['username'] = user.username
                    data = super().validate(attrs)
                except AuthenticationFailed as e:
                    raise AuthenticationFailed({'success': False, 'msg':'Invalid credentials'})

        return data


class GroceryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroceryItem
        fields = '__all__'  

class GroceryListSerializer(serializers.ModelSerializer):
    items = GroceryItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = GroceryList
        fields = ['id', 'name', 'items']
