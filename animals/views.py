from django.shortcuts import render
from .models import Record
from django.shortcuts import redirect
from django.db import connection

def mainpage(request):
    search_text = request.GET.get('text')
    if not search_text:
        return render(request,"main.html", {'data': Record.objects.filter(status_rec = 'добавлено'),'search_text':search_text}) 
    else:
        return render(request,"main.html", {'data': Record.objects.filter(status_rec = 'добавлено', rec_name__startswith = search_text), 'search_text':search_text})

def animal(request, id): 
    return render(request, "features.html", {'an' : Record.objects.get(record_id = id)})

def delete_rec(request, id):
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE animals_record SET status_rec = 'удалено' WHERE record_id = {id};")
    return redirect('http://127.0.0.1:8000/animals/')

# Create your views here.
