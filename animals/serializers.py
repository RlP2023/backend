from .models import Animal, Record, Record_of_Animal
from rest_framework import serializers

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Animal
        # Поля, которые мы сериализуем
        fields = ["animal_id", "an_name", "class_an", "result", 
        "status", "start_date","in_work",'end_date', "moderator", "creator"]

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Record
        # Поля, которые мы сериализуем
        fields = ["record_id", "rec_name", "units", "env_measur", 
        "description", "status_rec"]
    
class Record_of_AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Record_of_Animal
        # Поля, которые мы сериализуем
        fields = ["record_id", "animal_id", "description_rec"]
