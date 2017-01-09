import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render


def scrap(request):
    html = urlopen("https://www.avito.ru/perm/avtomobili/vaz_lada?user=1")
    bsObj = BeautifulSoup(html)
    model_list = bsObj.find("select", {"id": "flt_param_280"}).find_all("option")

    return render(request, 'base.html', {'model_list': model_list})


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)