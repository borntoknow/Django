
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.shortcuts import render
from scraper.models import CarName, Year, Car, BodyType


def scrap(request):

    # Удаляем все из таблиц
    CarName.objects.all().delete()
    Year.objects.all().delete()
    BodyType.objects.all().delete()
    Car.objects.all().delete()

    # Создаем объект BS
    html = urlopen("https://www.avito.ru/perm/avtomobili/vaz_lada?user=1")
    bs_obj = BeautifulSoup(html)

    # car_name = bs_obj.find("select", {"id": "flt_param_280"}).find_all("option")
    # for name in car_name:
    #     CarName(name=name.text.strip()).save()
    #
    # year_list = bs_obj.find("div", {"id": "param_188_from"}).find_all("option")
    # for year in year_list:
    #     Year(name=year.text).save()
    #
    # body_type_list = bs_obj.find("div", {"id": "param_187"}).find_all("option")
    # for type in body_type_list:
    #     BodyType(name=type.text).save()

    # Выбираем блоки с нужной информацией
    car_list = bs_obj.find("body").\
        find_all("div", {"class": "item item_table clearfix js-catalog-item-enum c-b-0 item_table_9"})

    # Выбираем из блока нужные нам поля
    for items in car_list:
        car_name = items.find("a", {"class": "item-description-title-link"}).text.split(",")[0].strip()
        year = items.find("a", {"class": "item-description-title-link"}).text.split(",")[1].strip()
        car_price = items.find("div", {"class": "about"}).text.split(".")[0].strip()
        body_type = items.find("span", {"class": "param"}).text.split(',')[2].strip()
        mileage = items.find("span", {"class": "param"}).text.split(",")[0].strip()
        pic_url = items.find("a", {"class": "photo-wrapper js-photo-wrapper"}, href=True)
        # Пишем в табличку car
        Car(car_name=car_name, year=year, price=car_price, body_type=body_type, mileage=mileage).save()

    # Выбиреам уникальные значения по полю car_name из car и пишем в carName
    names = Car.objects.values_list("car_name", flat=True).distinct().order_by("car_name")
    for name in names:
        CarName(name=name).save()

    # Выбиреам уникальные значения по полю year из car и пишем в year
    years = Car.objects.values_list("year", flat=True).distinct().order_by("year")
    for year in years:
        Year(name=year).save()

    # Выбиреам уникальные значения по полю body_type из car и пишем в bodyType
    body_types = Car.objects.values_list("body_type", flat=True).distinct().order_by("body_type")
    for body_type in body_types:
        BodyType(name=body_type).save()

    # Выбираем все из табличек и отправляем на стрничку
    scrap_list = Car.objects.all()
    filter_year = Year.objects.all()
    filter_body_type = BodyType.objects.all()
    filter_car_name = CarName.objects.all()
    return render(request, 'base.html', {"list": scrap_list,
                                         "filter_year": filter_year,
                                         "filter_body_type": filter_body_type,
                                         "filter_car_name": filter_car_name})


def do_filter(request):
    # Получаем параметры из запросв
    body_type = request.GET['body_type']
    year = request.GET['year']
    car_name = request.GET['car_name']

    # Делаем выборку из базы
    filter_list = Car.objects.filter(year__contains=year, body_type__contains=body_type, car_name__contains=car_name)

    # Рисуем страничку
    return render(request, "base.html", {"list": filter_list})


