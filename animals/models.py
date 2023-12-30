from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
    is_manager = models.BooleanField(default = False)

    def str(self):
        return self.username

class Record(models.Model):
    record_id = models.AutoField(primary_key = True)
    rec_name = models.CharField(max_length = 50)
    photo_record = models.BinaryField(editable=True, null = True,blank=True)
    units = models.CharField(max_length = 50)
    env_measur = models.CharField(max_length = 50)
    description = models.TextField()
    status_rec = models.CharField(max_length = 50)

class Animal(models.Model):
    animal_id = models.AutoField(primary_key = True)
    an_name = models.CharField(max_length = 50,blank = True,null = True)
    photo_animal = models.BinaryField(editable=True,blank = True,null = True)
    class_an = models.CharField(max_length = 50,blank = True,null = True)
    result = models.IntegerField(blank = True,null = True)
    status = models.CharField(max_length = 20)
    start_date = models.DateField(blank = True, null = True)
    in_work = models.DateField(blank = True, null = True)
    end_date = models.DateField(blank = True, null = True)
    moderator = models.ForeignKey(Custom_User, on_delete = models.CASCADE, related_name = 'moder',blank = True, null = True)
    creator = models.ForeignKey(Custom_User, on_delete = models.CASCADE, related_name = 'creator')

class Record_of_Animal(models.Model):
    record_id = models.ForeignKey(Record, on_delete = models.CASCADE)
    animal_id = models.ForeignKey(Animal, on_delete = models.CASCADE)
    description_rec = models.TextField()



# Create your models here.

