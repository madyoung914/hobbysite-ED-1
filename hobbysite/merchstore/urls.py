from django.urls import path
from .views import ProductTypeListView, ProductDetailView

urlpatterns = [
    path('items', ProductTypeListView.as_view(), name = "merchstore-list"),
    path('item/<int:pk>', ProductDetailView.as_view(), 
         name = "merchstore-item"),
]

app_name = "merchstore"
