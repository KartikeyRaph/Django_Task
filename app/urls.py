from django.urls import path, include
from .views import RegisterUser, MyTokenObtainPairView, GroceryItemListView, GroceryItemDetailView, GrocerylistListView, GrocerylistDetailView
from rest_framework_simplejwt.views import TokenRefreshView

# from .views import 

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('grocery-item/', GroceryItemListView.as_view(), name='grocery_item_list'),
    path('grocery-item/<int:pk>/', GroceryItemDetailView.as_view(), name='grocery_item_detail'),
    path('grocery-list/', GrocerylistListView.as_view(), name='grocery_list_list'),
    path('grocery-list/<int:pk>/', GrocerylistDetailView.as_view(), name='grocery_list_detail'),

]