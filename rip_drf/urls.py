from django.contrib import admin
from animals import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    
    path(r'records/', views.get_all_records, name='all-records-list'),
    path(r'records/<int:record_id>/', views.get_one_record, name='record-detail'),
    path(r'records/add/', views.add_record, name='add-record-post'),
    path(r'records/<int:record_id>/put/', views.put_detail, name='record-put'),
    path(r'records/<int:record_id>/delete/', views.delete_record, name='delete-record'),
    path(r'records/<int:record_id>/post/',views.add_record_to_animal, name='add-record'),

    path(r'animals/', views.get_all_animals, name='all-animals-list'),
    path(r'animals/form_animal/', views.form_animal, name='form-animal'),
    path(r'animals/delete_animal/', views.delete_animal, name='delete-animal'),
    path(r'animals/<int:animal_id>/get/', views.get_one_animal, name='get_one_animal'),
    path(r'animals/<int:animal_id>/approve_animal/', views.approve_animal, name='approve-animal'),
    path(r'animals/<int:animal_id>/decline_animal/', views.decline_animal, name='decline-animal'),
    path(r'animals/change_animal/', views.change_animal, name='change_animal'),


    path(r'links/delete_animal/<int:record_id>/', views.delete_animal, name='delete-animal'),
    path(r'links/change_desc/<int:record_id>/', views.change_desc, name='change_desc'),


    path('admin/', admin.site.urls),
]
