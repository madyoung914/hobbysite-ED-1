from django.shortcuts import render
from .models import Product, ProductType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class ProductTypeListView(ListView):
    model = ProductType
    template_name = "merchstore/merch_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/merch_detail.html"
