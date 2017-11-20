from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from App.models import ProType, Product


def index(request):
    data = Product.objects.all()
    type_list = ProType.objects.all()
    pro_paginator = Paginator(data, 20)

    context = {

        'data': pro_paginator.page(1).object_list,
        'typelist': type_list,
        'paginator': pro_paginator,
    }

    return render(request, 'index.html', context)


def classify(request, type_name=''):
    data = Product.objects.filter(ptype__name=type_name).all()
    type_list = ProType.objects.all()
    pro_paginator = Paginator(data, 20)

    context = {

        'data': pro_paginator.page(1).object_list,
        'typelist': type_list,
        'paginator': pro_paginator,

    }

    return render(request, 'index.html', context)
