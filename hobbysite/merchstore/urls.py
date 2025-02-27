from django.urls import path

from .views import merch_list, merch_detail, index

urlpatterns = [
    path('', index, name='index'),
    path('merchstore/items', merch_list, name = "merchstore-items"),
    path('merchstore/item/1', merch_detail, name = "merchstore-item"),
]

app_name = "merchstore"