from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import AnimalSerializer, RecordSerializer, Record_of_AnimalSerializer, Custom_User_Serializer
from .models import Animal, Record, Record_of_Animal,Custom_User
from rest_framework.decorators import api_view
import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import uuid
from django.conf import settings
import redis
from drf_yasg.utils import swagger_auto_schema
import json
from collections import OrderedDict
import ast
import requests
from django.contrib.auth import  logout


session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
ServerToken = 'abcde'
async_url = 'http://127.0.0.1:9000/'

def get_user_id():
  return 1

def get_user_id_mod():
  return 1

# услуги
@api_view(['Get'])
def get_all_records(request, format=None):
    try:
      ssid = request.headers["authorization"]
    except:
      ssid = ''
    print(ssid)
    if ssid and Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):
      user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
      if Animal.objects.filter(creator=user, status='Forming'):
        draft_id = Animal.objects.get(creator=user, status='Forming').animal_id
        records = Record.objects.filter(status_rec="Добавлено")
        if request.GET.get('name_filter'):
          records=Record.objects.filter(rec_name__startswith = request.GET.get('name_filter').capitalize(),status_rec="Добавлено")
        serializer = RecordSerializer(records, many=True)
        d = dict()
        d['draft_id'] = draft_id
        d['data']= serializer.data
        return Response(d)

    records = Record.objects.filter(status_rec="Добавлено")
    if request.GET.get('name_filter'):
      records=Record.objects.filter(rec_name__startswith = request.GET.get('name_filter').capitalize(),status_rec="Добавлено")
    serializer = RecordSerializer(records, many=True)
    d = dict()
    d['data'] = serializer.data
    d['draft_id'] = -1
    return Response(d)

 
@api_view(['Get'])
def get_one_record(request, record_id, format=None):
    record = get_object_or_404(Record, record_id=record_id)
    if request.method == 'GET':
        serializer = RecordSerializer(record)
        return Response(serializer.data)

@api_view(['Post'])
def add_record(request, format=None):    
    try:
        ssid = request.headers["authorization"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:
      print('post')
      d = {k:v for k,v in list(request.data.items())}
      d['status_rec'] = 'Добавлено'
      try:
        d['photo_record'] = d['photo_record'][d['photo_record'].index('/9j'):]
      except:
        pass
      serializer = RecordSerializer(data=d)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['Put'])
def put_detail(request, record_id, format=None):
    try:
        ssid = request.headers["authorization"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:
      d = {}
      record = get_object_or_404(Record, record_id=record_id)
      d["rec_id"] = record_id
      d = {k:v for k,v in list(request.data.items())}
      try:
        d['photo_record'] = d['photo_record'][d['photo_record'].index('/9j'):]
      except:
        pass
      serializer = RecordSerializer(record, data=d,partial=True)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_record(request, record_id, format=None):   
    try:
        ssid = request.headers["authorization"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:
      record = get_object_or_404(Record, record_id=record_id)
      Record.objects.filter(record_id=record_id).update(status_rec='F')
      return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['Post'])
def add_record_to_animal(request, record_id, format=None):
    try:
        ssid = request.headers["authorization"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):
      record= get_object_or_404(Record, record_id=record_id)
      if Animal.objects.filter(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming'):
        pass
      else:
        Animal.objects.create(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming',start_date=datetime.datetime.now())
      Record_of_Animal.objects.create(record_id = record, animal_id = Animal.objects.get(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming'))
      return Response(status=status.HTTP_204_NO_CONTENT)


# заявки
@api_view(['Get'])
def get_all_animals(request, format=None):
    try:
      ssid = request.headers["authorization"]
    except:
      ssid = request.COOKIES['session_id']
    print(ssid)
    if ssid and Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:
      beg = request.GET.get('begin_of_int')
      end = request.GET.get('end_of_int')
      try:
        status_param =  request.GET.get('status').split(',')
      except:
        status_param = ['Forming','Decline','Active','Aprove']
      if beg:
        animals = Animal.objects.filter(in_work__gte=beg)
      if end:
        animals = Animal.objects.filter(in_work__lte=end)
      if beg and end:
        animals = Animal.objects.filter(in_work__range=(beg, end))
      if not (beg or end):
        animals = Animal.objects.all()
      if status_param:
        animals = animals.filter(status__in=status_param)
      serializer = AnimalSerializer(animals, many=True)
      return Response(serializer.data)
    elif Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]) is not None:
      user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
      beg = request.GET.get('begin_of_int')
      end = request.GET.get('end_of_int')
      try:
        status_param =  request.GET.get('status').split(',')
      except:
        status_param = ['Forming','Decline','Active','Aprove']
      if beg:
        animals = Animal.objects.filter(in_work__gte=beg,creator=user)
      if end:
        animals = Animal.objects.filter(in_work__lte=end,creator=user)
      if not (beg or end):
        animals = Animal.objects.filter(creator=user)
      if beg and end:
        animals = Animal.objects.filter(in_work__range=(beg, end),creator=user)
      
      if status_param:
        animals = animals.filter(status__in=status_param)
      serializer = AnimalSerializer(animals, many=True)
      return Response(serializer.data)
    else:
      return Response(status=status.HTTP_403_FORBIDDEN)


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
def approve_or_decline_animal(request,animal_id, format=None):
    try:
        ssid = request.headers["authorization"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]).is_manager:
      statu = request.data['status']
      animal = get_object_or_404(Animal, animal_id=animal_id)
      user = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1])
      if animal.status != 'Active':
        return Response(status=status.HTTP_412_PRECONDITION_FAILED)
      Animal.objects.filter(animal_id=animal_id).update(status=statu,end_date = datetime.datetime.now(),moderator = Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]))
      return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['Put'])
def form_animal(request, format = None):
    try:
        ssid = request.headers["authorization"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):
      if Animal.objects.filter(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming'):
        go_to_async(Animal.objects.get(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming'))
        Animal.objects.filter(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming').update(status = 'Active',in_work=datetime.datetime.now())
        return Response(status=status.HTTP_204_NO_CONTENT)
      return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['Delete'])
def delete_animal(request, format = None):
    try:
        ssid = request.headers["authorization"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):
      if Animal.objects.filter(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming'):
        Animal.objects.filter(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming').update(status = 'Deleted')
        return Response(status=status.HTTP_204_NO_CONTENT)
      return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_404_NOT_FOUND)

# ссылки м-м

@api_view(['Delete'])
def delete_animal_record(request, record_id, format=None):
  try:
      ssid = request.headers["authorization"]
  except:
      print('ÁAAAAA')
      return Response(status=status.HTTP_403_FORBIDDEN)
  print("AA")
  if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]) is not None:
    print("AA")
    order = Animal.objects.get(status="Forming",creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]))
    record = get_object_or_404(Record_of_Animal, record_id=Record.objects.get(record_id=record_id), animal_id=order)
    if Animal.objects.get(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming'):
      record = get_object_or_404(Record_of_Animal,record_id = Record.objects.get(record_id=record_id),animal_id = Animal.objects.get(creator=Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]), status='Forming'))
      record.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

    else:
      return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)
  return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['Put'])
def change_animal(request, format = None):
    try:
        ssid = request.headers["authorization"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):
      user = get_object_or_404(Custom_User, username = str(session_storage.get(ssid))[2:-1])

      if Animal.objects.filter(creator=user, status='Forming'):
        d = {}
        animal = Animal.objects.filter(creator=user, status='Forming')[0]
        d = {k:v for k,v in list(request.data.items())}
        try:
          d['photo_animal'] = d['photo_animal'][d['photo_animal'].index('/9j'):]
        except:
          pass
        serializer = AnimalSerializer(animal, data=d,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def go_to_async(animal):
  payload = {}
  payload['animal_id'] = animal.animal_id
  try:
    requests.put(async_url,data=json.dumps(payload),)
  except:
    print("Не могу достучаться")



@api_view(['Put'])
def update_animal_async(request):
  print(request.data)
  if request.data['Server-Token'] == ServerToken:
    animal = get_object_or_404(Animal, animal_id=request.data['animal_id'])
    serializer = AnimalSerializer(animal, data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  else:
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['Put'])
def change_desc(request, record_id, format = None):
    try:
        ssid = request.COOKIES["session_id"]
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if Custom_User.objects.get(username = str(session_storage.get(ssid))[2:-1]):
      user = get_object_or_404(Custom_User, username = str(session_storage.get(ssid))[2:-1])
      if Animal.objects.filter(creator=user, status='Forming'):
        animal = Animal.objects.get(creator=user, status='Forming')
        record = get_object_or_404(Record, record_id=record_id)
        row = get_object_or_404(Record_of_Animal, record_id=record, animal_id=animal)
        Record_of_Animal.objects.filter(record_id=record, animal_id=animal).update(description_rec = request.data['description_rec'])
        return Response(status=status.HTTP_204_NO_CONTENT)
      else:
        return Response(status=status.HTTP_404_NOT_FOUND)


#############################
@swagger_auto_schema(method='post',request_body=Custom_User_Serializer)
@api_view(['Post'])
def authorize(request):
    print(request.data)
    username = request.data["username"] # допустим передали username и password
    password = request.data["password"]
    user = authenticate(request, username=username, password=password)
    print(username)
    print(password)
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)
        
        response = Response({'session_id':random_key,'username':username,'is_moderator':Custom_User.objects.get(username=username).is_manager,"user_id":Custom_User.objects.get(username=username).id})
        print(response.data)
        response.set_cookie("session_id", random_key) # пусть ключем для куки будет session_id
        return response
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='post',request_body=Custom_User_Serializer)
@api_view(['Post'])
def create_account(request):
	username = request.data["username"]
	email = request.data["email"]
	passwd = request.data["password"]
	try:
		Custom_User.objects.create_user(username = username, email = email, password = passwd)
		return HttpResponse("{'status': 'ok'}")
	except:
		return HttpResponse("{'status': 'error', 'error': 'wrong data'}")
@swagger_auto_schema(method='post')
@api_view(['Post'])
def logout_view(request):
  print(request.headers)
  try:
    ssid = request.headers["authorization"]
  except:
    return Response(status=status.HTTP_401_UNAUTHORIZED)
  try:
    Animal.objects.get(status="Forming",creator=Custom_User.objects.get(username=session_storage.get(ssid).decode('utf-8'))).delete()
  except:
    pass
  session_storage.delete(ssid)

  logout(request._request)
  response = HttpResponse(status=status.HTTP_200_OK)
  response.delete_cookie("session_id")
  return response
