from django.urls import path
from .views import ProductCreateView, ProductTypeListView, ProductDetailView, ProductUpdateView

urlpatterns = [
    path('items', ProductTypeListView.as_view(), name ="merchstore-list"),
    path('item/<int:pk>', ProductDetailView.as_view(),
         name="merchstore-item"),
    path('item/add', ProductCreateView.as_view(), name="merch-add"),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name="merch-edit"),
]

app_name = "merchstore"
