from django.urls import path

from .views import ProductTypeListView, ProductDetailView

urlpatterns = [
    #path('', index, name='index'),
    path('merchstore/items', ProductTypeListView.as_view(), name = "merchstore-list"),
    path('merchstore/item/<int:pk>', ProductDetailView.as_view(), name = "merchstore-item"),
]

app_name = "merchstore"