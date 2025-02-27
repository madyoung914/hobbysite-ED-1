from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 

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
