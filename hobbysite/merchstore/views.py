from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product, ProductType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm, TransactionForm


class ProductTypeListView(ListView):
    model = ProductType
    template_name = "merchstore/merch_list.html"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "merchstore/merch_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = TransactionForm()
        return ctx
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = self.object
            transaction.buyer = request.user.profile
            transaction.status = 'CART'
            transaction.save()
            return redirect(reverse('merchstore:merchstore-item', kwargs={'pk': self.object.pk}))
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/merch_add.html"


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/merch_edit.html"
