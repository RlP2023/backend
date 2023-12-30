from django.shortcuts import render

class animals():
    def __init__ (self, id, name, typeof, number, photo, record, family, inf):
        self.id = id
        self.name = name
        self.typeof = typeof
        self.number = number
        self.photo = photo
        self.record = record
        self.family = family
        self.inf = inf
        
mas = []
mas.append(animals(1, 'Синий кит', 'Млекопитающие', 10000, 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Anim1754_-_Flickr_-_NOAA_Photo_Library.jpg/1280px-Anim1754_-_Flickr_-_NOAA_Photo_Library.jpg',
    'Самое крупное животное', 'Семейство: Полосатиковые', 'Его длина достигает 33 метров, а масса может значительно превышать 150 тонн'))
mas.append(animals(2, 'Гепард', 'Млекопитающие', 7000, 'https://vektor-tv.ru/upload/images/IZ/animals%20extra/cheetah-gc2f923a8b_1280.jpg', 
    'Самое быстрое животное', 'Семейство: Кошачьи', 'За 3 секунды может развивать скорость до 110 км/ч'))
mas.append(animals(3, 'Медоед', 'Млекопитающие', 10000, 'https://faunistics.com/wp-content/uploads/2022/01/1-1.jpg', 
    'Самое храброе животное', 'Семейство: Куньи', 'Очень толстая и жесткая кожа не позволяет более крупным зверям нанести какой-то ощутимый урон'))

def mainpage(request):
    search_text = request.GET.get('text')
    if not search_text:
        return render(request,"main.html", {'data': mas}) 
    else:
        search_animals = []
        for an in mas:
            if an.record.lower().startswith(search_text.lower()):
                search_animals.append(an)
        return render(request,"main.html", {'data': search_animals})

def animal(request, id):
    for an in mas:
        if an.id == id:
            return render(request, "features.html", {'an' : an})

# Create your views here.
