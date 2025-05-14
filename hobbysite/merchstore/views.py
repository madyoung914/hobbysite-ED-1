from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from .models import Product, ProductType, Transaction
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm, TransactionForm
from user_management.models import Profile


class ProductTypeListView(ListView):
    model = ProductType
    template_name = "merchstore/merch_list.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            MadeProduct = self.request.user.profile.products.all().count() 
            OnSaleProduct = self.request.user.profile.products.filter(status='SALE').count()

            hasProduct = False
            hasSale = False

            if MadeProduct-OnSaleProduct >0:
                hasProduct = True
            if OnSaleProduct>0:
                hasSale = True
            ctx['hasProduct'] = hasProduct
            ctx['hasSale'] = hasSale

        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/merch_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = TransactionForm()
        return ctx

    def process_transaction_form(self, form_data):
        form = TransactionForm(form_data)
        if form.is_valid() and form.instance.amount <= self.object.stock and form.instance.amount != 0:
            self.object.stock -= form.instance.amount

            transaction = form.save(commit=False)
            transaction.product = self.object
            transaction.buyer = self.request.user.profile

            if self.object.stock == 0:
                self.object.status = 'OOS'

            transaction.status = 'CART'

            transaction.save()
            self.object.save()

            return redirect(reverse('merchstore:merch-cart'))
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.is_authenticated and 'temporary' in request.session:
            saved_data = request.session.pop('temporary')
            return self.process_transaction_form(saved_data)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            request.session['temporary'] = request.POST.dict()
            return redirect('%s?next=%s' % (reverse('login'), request.path))

        return self.process_transaction_form(request.POST)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/merch_add.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        if form.instance.sale_percent:
                form.instance.sale_price = form.instance.price - (form.instance.price * (form.instance.sale_percent)/100)
                form.instance.status = 'SALE'
        else:
            form.instance.status = 'AVL'

        if form.instance.stock == 0:
            form.instance.status = 'OOS'
            
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("merchstore:merchstore-item",
                            kwargs={"pk": self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/merch_edit.html"

    def form_valid(self, form):
        if form.instance.sale_percent:
                form.instance.sale_price = self.object.price - (self.object.price * (form.instance.sale_percent)/100)
                form.instance.status = 'SALE'
        else:
            form.instance.status = 'AVL'

        if form.instance.stock == 0:
            form.instance.status = 'OOS'
            
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("merchstore:merchstore-item",
                            kwargs={"pk": self.object.pk})


class CartView (LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/cart.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        transaction_buyer = Profile.objects.get(user=self.request.user)
        ctx['user_transactions'] = Transaction.objects.filter(buyer = transaction_buyer)
        return ctx


class TransactionListView (LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/transaction.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        transaction_owner = Profile.objects.get(user=self.request.user)
        
        ctx['user_transactions'] = Transaction.objects.filter(product__owner = transaction_owner).order_by('-created_on')

        return ctx
