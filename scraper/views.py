import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from scraper.models import CarName, Year, Car, BodyType


def scrap(request):

    CarName.objects.all().delete()
    Year.objects.all().delete()
    BodyType.objects.all().delete()
    Car.objects.all().delete()

    html = urlopen("https://www.avito.ru/perm/avtomobili/vaz_lada?user=1")
    bs_obj = BeautifulSoup(html)

    car_name = bs_obj.find("select", {"id": "flt_param_280"}).find_all("option")
    for name in car_name:
        CarName(name=name.text.strip()).save()

    year_list = bs_obj.find("div", {"id": "param_188_from"}).find_all("option")
    for year in year_list:
        Year(name=year.text).save()

    body_type_list = bs_obj.find("div", {"id": "param_187"}).find_all("option")
    for type in body_type_list:
        BodyType(name=type.text).save()

    car_list = bs_obj.find("body").find_all("a", {"class": "item-description-title-link"})
    for items in car_list:
        Car(car_name=CarName.objects.get(name=items.text.split(",")[0].strip()).id).save()

        # Car(year=items.text.split(",")[1]).save()

    return render(request, 'base.html')


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)