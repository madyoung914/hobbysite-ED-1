from django.shortcuts import render
from .models import Product, ProductType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm


class ProductTypeListView(ListView):
    model = ProductType
    template_name = "merchstore/merch_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/merch_detail.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/merch_add.html"
