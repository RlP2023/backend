from django.contrib import admin
from .models import *
from django import forms
import base64

admin.site.register(Custom_User)
admin.site.register(Record_of_Animal)


class BinaryField(forms.FileField):
    def to_python(self, data):
        data = super().to_python(data)
        if data:
            data = base64.b64encode(data.read()).decode('ascii')
        return data

class BinaryFileInputAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.BinaryField: {'form_class': BinaryField},
    }
admin.site.register(Record, BinaryFileInputAdmin)
admin.site.register(Animal, BinaryFileInputAdmin)
# Register your models here.
