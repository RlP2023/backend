from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
    is_manager = models.BooleanField(default = False)

    def str(self):
        return self.username

class Record(models.Model):
    record_id = models.AutoField(primary_key = True)
    rec_name = models.CharField(max_length = 50)
    photo_url = models.CharField(max_length = 500)
    units = models.CharField(max_length = 50)
    env_measur = models.CharField(max_length = 50)
    description = models.TextField()
    status_rec = models.CharField(max_length = 50)

class Animal(models.Model):
    animal_id = models.AutoField(primary_key = True)
    an_name = models.CharField(max_length = 50)
    photo_url_an = models.CharField(max_length = 500)
    class_an = models.CharField(max_length = 50)
    result = models.IntegerField()
    status_an = models.CharField(max_length = 50)
    moderator = models.ForeignKey(Custom_User, on_delete = models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)

class Record_of_Animal(models.Model):
    record_id = models.ForeignKey(Record, on_delete = models.CASCADE)
    animal_id = models.ForeignKey(Animal, on_delete = models.CASCADE)
    description_rec = models.TextField()



# Create your models here.
