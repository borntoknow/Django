# Django
Аннотация

	В данной работе продемонстрировано использование методики и технологии, создания приложения на основе архитектуры MVC.

	Показано, как с помощью языка программирования «Python» и Фреймворка «Django» можно в кратчайшие сроки разрабатывать и развертывать WEB приложения.

	Демонстрационное приложение, созданное для данной работы, представляет собой простейшее однопользовательское WEB приложение для синтаксического анализа, структурирования, сбора и хранения информации в БД с ресурсов, размещенных в сети «интернет» с использованием библиотеки «BeatifulSoup».

	В качестве среды разработки был выбран продукт «PyCharm 2016» и база данных SQLLite.

Задание

Спроектировать и разработать приложение для подбора товаров(автомобилей) по параметрам.

Используемый источник данных сайт avito.ru раздел автотранспорт.

Решение

Для создания приложения было создано три модели (таблицы):

1.	Car с полями 
•	сar_name – название машины
•	year – год выпуска
•	body_type – тип кузова
•	price – цена
•	mileage -  пробег
2.	CarName c полями 
•	name 
3.	Year с полями 
•	name 
4.	BodyType c полями
•	name 

Код реализующий модели: 

 class CarName (models.Model):
    name = models.CharField(max_length=50)

class Year (models.Model):
    name = models.CharField(max_length=10)

class BodyType (models.Model):
    name = models.CharField(max_length=50)

class Car (models.Model):
    car_name = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    mileage = models.CharField(max_length=6)
    pic_url = models.CharField(max_length=50)

Для сбора данных из источника первоначально были выбраны все блоки с интересующей нас информацией, с помощью кода:

  html = urlopen("https://www.avito.ru/perm/avtomobili/vaz_lada?user=1")
    bs_obj = BeautifulSoup(html)

    # Выбираем блоки с нужной информацией
    car_list = bs_obj.find("body").\
        find_all("div", {"class": "item item_table clearfix js-catalog-item-enum c-b-0 item_table_9"})

Далее из этих блоков выбраны нужные нам поля, код:

    for items in car_list:
        car_name = items.find("a", {"class": "item-description-title-link"}).text.split(",")[0].strip()
        year = items.find("a", {"class": "item-description-title-link"}).text.split(",")[1].strip()
        car_price = items.find("div", {"class": "about"}).text.split(".")[0].strip()
        body_type = items.find("span", {"class": "param"}).text.split(',')[2].strip()
        mileage = items.find("span", {"class": "param"}).text.split(",")[0].strip()
        pic_url = items.find("a", {"class": "photo-wrapper js-photo-wrapper"}, href=True)

И сохраняем информацию в созданной ранее модели Car:

Car(car_name=car_name, year=year, price=car_price, body_type=body_type, mileage=mileage).save()

Для создания фильтров было решено взять уникальные поля из выборки и поместить их в созданные модели: 

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

Передаем информацию на страницу:

# Выбираем все из табличек и отправляем на стрничку
    scrap_list = Car.objects.all()
    filter_year = Year.objects.all()
    filter_body_type = BodyType.objects.all()
    filter_car_name = CarName.objects.all()
    return render(request, 'base.html', {"list": scrap_list,
                                         "filter_year": filter_year,
                                         "filter_body_type": filter_body_type,
                                         "filter_car_name": filter_car_name})


Для выбора дынных по созданным нами полям используем метод получающий параметры со страницы и производящий по ним выборку из модели:

# Получаем параметры из запросв
    body_type = request.GET['body_type']
    year = request.GET['year']
    car_name = request.GET['car_name']

    # Делаем выборку из базы
    filter_list = Car.objects.filter(year__contains=year, body_type__contains=body_type, car_name__contains=car_name)

    # Рисуем страничку
    return render(request, "base.html", {"list": filter_list})


