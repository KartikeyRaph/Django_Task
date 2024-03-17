from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, MyTokenObtainPairSerializer, GroceryItemSerializer, GroceryListSerializer
from .models import GroceryItem, GroceryList
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.db import IntegrityError 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated



class RegisterUser(APIView):

    def post(self, request):

        if User.objects.filter(email =request.data['email']):
            return Response({"success" : False, "message": "User with this Email already exists. "}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                user  = serializer.save()
                refresh = RefreshToken.for_user(user)
                response_data = {
                    "success" : True,
                    "message": "User created successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }

                GroceryList.objects.create(user=user, name = "Default grocery list")

                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"success" : False, "error": "Username already exists."}, status=status.HTTP_409_CONFLICT)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@permission_classes([IsAuthenticated])
class GroceryItemListView(APIView):

    def get(self, request):
        queryset = GroceryItem.objects.all()
        serializer = GroceryItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroceryItemSerializer(data=request.data)
        if serializer.is_valid():
            grocery_item = serializer.save()
            
            # Creating recording for many o many field
            user = User.objects.get(username = request.user)
            grocery_list = GroceryList.objects.get(user=user)
            grocery_list.items.add(grocery_item)
            grocery_list.save()

            response_data = {
                    "success" : True,
                    "message": "Item created successfully",
                }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class GroceryItemDetailView(APIView):

    def get(self, request, pk):
        try:
            instance = self.get_object(pk)
            serializer = GroceryItemSerializer(instance)
            return Response(serializer.data)
        except GroceryItem.DoesNotExist:
            return Response({"success": False,"message": "Grocery item not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self, pk):
        try:
            return GroceryItem.objects.get(pk=pk)
        except GroceryItem.DoesNotExist:
            raise GroceryItem.DoesNotExist

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = GroceryItemSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                    "success" : True,
                    "message": "Item updated successfully",
                }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(username = request.user)
            grocery_item = GroceryItem.objects.get(id=pk)
            grocery_list = GroceryList.objects.get(name  = "Default grocery list", user_id = user.id, items = grocery_item)
        except (GroceryList.DoesNotExist, GroceryItem.DoesNotExist):
            return Response({"success": True, "message": "Grocery list or item not found."}, status=status.HTTP_404_NOT_FOUND)
        
        grocery_list.items.remove(grocery_item)
        
        return Response({"success": True,"message": "Item removed successfully."}, status=status.HTTP_200_OK)
    


@permission_classes([IsAuthenticated])
class GrocerylistListView(APIView):

    def get(self, request):
        queryset = GroceryList.objects.filter(user = request.user)
        serializer = GroceryListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroceryListSerializer(data=request.data)
        if serializer.is_valid():
            grocery_list = serializer.save(user = request.user)
            
            grocery_items = GroceryItem.objects.filter(id__in=request.data['items'])
            grocery_list.items.add(*grocery_items)
            grocery_list.save()

            response_data = {
                    "success" : True,
                    "message": "List created successfully",
                }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class GrocerylistDetailView(APIView):

    def get(self, request, pk):
        try:
            instance = self.get_object(pk)
            serializer = GroceryListSerializer(instance)
            return Response(serializer.data)
        except GroceryList.DoesNotExist:
            return Response({"success": False,"message": "Grocery list not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_object(self, pk):
        try:
            return GroceryList.objects.get(pk=pk)
        except GroceryList.DoesNotExist:
            raise GroceryList.DoesNotExist

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = GroceryListSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            grocery_list = serializer.save()

            grocery_items = GroceryItem.objects.filter(id__in=request.data['items'])
            grocery_list.items.add(*grocery_items)
            grocery_list.save()

            response_data = {
                    "success" : True,
                    "message": "List updated successfully",
                }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            instance = GroceryList.objects.get(id = pk)
            instance.delete()
        except (GroceryList.DoesNotExist):
            return Response({"success": True, "message": "Grocery list not found."}, status=status.HTTP_404_NOT_FOUND)
                
        return Response({"success": True,"message": "List removed successfully."}, status=status.HTTP_200_OK)