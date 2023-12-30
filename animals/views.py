from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import AnimalSerializer, RecordSerializer, Record_of_AnimalSerializer
from .models import Animal, Record, Record_of_Animal,Custom_User
from rest_framework.decorators import api_view
import datetime

def get_user_id():
  return 1

def get_user_id_mod():
  return 1

@api_view(['Get'])
def get_all_records(request, format=None):
    print('get')
    records = Record.objects.all()
    serializer = RecordSerializer(records, many=True)
    return Response(serializer.data)
    
@api_view(['Get'])
def get_one_record(request, record_id, format=None):
    record = get_object_or_404(Record, record_id=record_id)
    if request.method == 'GET':
        serializer = RecordSerializer(record)
        return Response(serializer.data)

@api_view(['Post'])
def add_record(request, format=None):    
    print('post')
    serializer = RecordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])
def put_detail(request, record_id, format=None):
    record = get_object_or_404(Record, record_id=record_id)
    serializer = RecordSerializer(record, data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_record(request, record_id, format=None):    
    record = get_object_or_404(Record, record_id=record_id)
    Record.objects.filter(record_id=record_id).update(status='F')
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['Post'])
def add_record_to_animal(request, record_id, format=None):
  user_id = get_user_id()
  record= get_object_or_404(Record, record_id=record_id)
  if Animal.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'):
    pass
  else:
    Animal.objects.create(creator=Custom_User.objects.get(id=user_id), status='Forming',start_date=datetime.datetime.now())
  Record_of_Animal.objects.create(record_id = record, animal_id = Animal.objects.get(creator=Custom_User.objects.get(id=user_id), status='Forming'))
  return Response(status=status.HTTP_204_NO_CONTENT)


# методы ЗАЯВОК !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

@api_view(['Get'])
def get_all_animals(request, format=None):
    animals= Animal.objects.all()
    serializer = AnimalSerializer(animals, many=True)
    return Response(serializer.data)

@api_view(['Get'])
def get_one_animal(request, animal_id,format = None):
  animal = get_object_or_404(Animal, animal_id=animal_id)
  if request.method == 'GET':
    serializer_animal = AnimalSerializer(animal)
    comp_list = []
    for record_of_animal in Record_of_Animal.objects.filter(animal_id=animal_id):
      temp = RecordSerializer(record_of_animal.record_id).data
      temp['desr'] = record_of_animal.description_rec
      comp_list.append(temp)
    cont = dict(serializer_animal.data)
    cont['records'] = comp_list
    return Response(cont)

@api_view(['Put'])
def approve_animal(request,animal_id, format=None):
  animal = get_object_or_404(Animal, animal_id=animal_id)
  user = Custom_User.objects.get(id=get_user_id_mod())
  if animal.moderator != user:
    return Response(status=status.HTTP_403_FORBIDDEN)
  if animal.status != 'Active':
    return Response(status=status.HTTP_412_PRECONDITION_FAILED)
  Animal.objects.filter(animal_id=animal_id).update(status='Finished',end_date = datetime.datetime.now())
  return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def decline_animal(request,animal_id, format=None):
  animal = get_object_or_404(Animal, animal_id=animal_id)
  user = Custom_User.objects.get(id=get_user_id_mod())
  if animal.moderator != user:
    return Response(status=status.HTTP_403_FORBIDDEN)
  if animal.status != 'Active':
    return Response(status=status.HTTP_412_PRECONDITION_FAILED)
  Animal.objects.filter(animal_id=animal_id).update(status='Declined',end_date=datetime.datetime.now())
  return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def form_animal(request, format = None):
  user_id = get_user_id()
  if Animal.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'):
    Animal.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming').update(status = 'Active',moderator = Custom_User.objects.get(id=get_user_id_mod()),in_work=datetime.datetime.now())
    return Response(status=status.HTTP_204_NO_CONTENT)
  return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['Put'])
def delete_animal(request, format = None):
  user_id = get_user_id()
  if Animal.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'):
    Animal.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming').update(status = 'Deleted')
    return Response(status=status.HTTP_204_NO_CONTENT)
  return Response(status=status.HTTP_404_NOT_FOUND)

# МЕТОДЫ ССЫЛОК М-М !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

@api_view(['Delete'])
def delete_animal(request, record_id, format=None):
  user_id = get_user_id()
  record = get_object_or_404(Record_of_Animal, record_id=record_id)
  if Animal.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'):
    record = get_object_or_404(Record_of_Animal,record_id = record,animal_id = Animal.objects.filter(creator=Custom_User.objects.get(id=user_id), status='Forming'))
    record.delete()
  else:
    return Response(status=status.HTTP_404_NOT_FOUND)
  return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['Put'])
def change_animal(request, format = None):
  user = get_object_or_404(Custom_User, id = get_user_id())
  if Animal.objects.filter(creator=user, status='Forming'):
    if request.data.get('an_name'):
      Animal.objects.filter(creator=user, status='Forming').update(an_name = request.data.get('an_name'))
    if request.data.get('photo_animal'):
      Animal.objects.filter(creator=user, status='Forming').update(photo_animal = request.data.get('photo_animal'))
    if request.data.get('class_an'):
      Animal.objects.filter(creator=user, status='Forming').update(class_an = request.data.get('class_an'))
    if request.data.get('result'):
      Animal.objects.filter(creator=user, status='Forming').update(result = request.data.get('result'))
    return Response(status=status.HTTP_204_NO_CONTENT)
  else:
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['Put'])
def change_desc(request, record_id, format = None):
  user = get_object_or_404(Custom_User, id = get_user_id())
  if Animal.objects.filter(creator=user, status='Forming'):
    animal = Animal.objects.get(creator=user, status='Forming')
    record = get_object_or_404(Record, record_id=record_id)
    row = get_object_or_404(Record_of_Animal, record_id=record, animal_id=animal)
    Record_of_Animal.objects.filter(record_id=record, animal_id=animal).update(description_rec = request.data['description_rec'])
    return Response(status=status.HTTP_204_NO_CONTENT)
  else:
    return Response(status=status.HTTP_404_NOT_FOUND)
