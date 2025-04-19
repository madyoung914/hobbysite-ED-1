from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from .models import Product, ProductType, Transaction
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm, TransactionForm
from django.contrib.auth import login


class ProductTypeListView(ListView):
    model = ProductType
    template_name = "merchstore/merch_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/merch_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = TransactionForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TransactionForm(request.POST)

        if form.is_valid() and form.instance.amount <= self.object.stock and form.instance.amount != 0:
            # but also submit button should not be clickable if stock is 0
            self.object.stock -= form.instance.amount

            user = request.user
            login(request, user)

            transaction = form.save(commit=False)
            transaction.product = self.object
            transaction.buyer = request.user.profile

            if self.object.stock == 0:
                self.object.status = 'OOS'

            transaction.status = 'CART'

            transaction.save()
            self.object.save()

            return redirect(reverse('merchstore:merch-cart'))
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/merch_add.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("merchstore:merchstore-item",
                            kwargs={"pk": self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/merch_edit.html"

    def form_valid(self, form):
        if form.instance.stock == 0:
            form.instance.status = 'OOS'
        elif form.instance.stock != 0 and form.instance.status == 'OOS':
            form.instance.status = 'AVL'

        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("merchstore:merchstore-item",
                            kwargs={"pk": self.object.pk})


class CartView (LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/cart.html"


class TransactionListView (LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/transaction.html"
