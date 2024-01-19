from .models import Animal, Record, Record_of_Animal, Custom_User
from rest_framework import serializers
from collections import OrderedDict

class AnimalSerializer(serializers.ModelSerializer):
    full_name_creator = serializers.SerializerMethodField()
    def get_full_name_creator(self, obj):
        return  obj.creator.username  
    full_name_mod = serializers.SerializerMethodField()
    def get_full_name_mod(self, obj):
        try:
            return obj.moderator.username
        except:
            return ""
    class Meta:
        # Модель, которую мы сериализуем
        model = Animal
        # Поля, которые мы сериализуем
        fields = ["animal_id", "an_name", "class_an", "result", 'animal_description','photo_animal',
        "status", "start_date","in_work",'end_date', "full_name_mod", "full_name_creator"]
    

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Record
        # Поля, которые мы сериализуем
        fields = ["record_id", "rec_name", "units", "photo_record", 
        "env_measur", "description", "status_rec"]
    
class Record_of_AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Record_of_Animal
        # Поля, которые мы сериализуем
        fields = ["record_id", "animal_id", "description_rec"]
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 

class Custom_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_User
        fields = ['username','email','password','is_manager']
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields


