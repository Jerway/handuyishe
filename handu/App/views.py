from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from App.models import ProType, Product
import math


def index(request):
    data = Product.objects.all()
    type_list = ProType.objects.all()
    pro_paginator = Paginator(data, 20)

    context = {

        'data': pro_paginator.page(1).object_list,
        'typelist': type_list,
        'paginator': pro_paginator,
        'present_page': 1,
        'type_name': 'all',

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
        'present_page': 1,
        'type_name': type_name

    }

    return render(request, 'index.html', context)


def page_chage(request, type_name, direction, present_page):
    if type_name == 'all':
        pro_object = Product.objects.all()
    else:
        pro_object = Product.objects.filter(ptype__name=type_name).all()
    pro_paginator = Paginator(pro_object, 20)
    if direction == '0':
        if present_page == '1':
            data = pro_paginator.page(1).object_list
            present_page = 1
        else:
            data = pro_paginator.page(int(present_page) - 1).object_list
            present_page = int(present_page) - 1
    else:
        if present_page == pro_paginator.num_pages:
            data = pro_paginator.page(pro_paginator.num_pages).object_list
            present_page = pro_paginator.num_pages
        else:
            data = pro_paginator.page(int(present_page) + 1).object_list
            present_page = int(present_page) + 1
    type_list = ProType.objects.all()

    context = {

        'data': data,
        'typelist': type_list,
        'paginator': pro_paginator,
        'present_page': present_page,
        'type_name': type_name

    }

    return render(request, 'index.html', context)
