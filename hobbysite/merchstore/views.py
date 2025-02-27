from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from .models import Product, ProductType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

class ProductTypeListView(ListView):
    model = ProductType
    template_name = "merch_list.html"

class ProductDetailView(DetailView):
    model = Product
    template_name = "merch_detail.html"

'''
def index(request):
    return HttpResponse(' ')

def merch_list(request):
    ctx = {
        "merchs": [
            'BTS',
            'Blackpink',
            'IVE',
            'New Jeans'
        ]
    }

    return render(request, 'merchstore/merch_list.html', ctx)

def merch_detail(request): 
    ctx = {
        "word": 'Hi'
    }
    return render(request, 'merchstore/merch_detail.html', ctx)
'''