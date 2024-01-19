from django.contrib import admin
from animals import views
from django.urls import include, path
from rest_framework import routers
from rest_framework import permissions
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    
    path(r'records', views.get_all_records, name='all-records-list'),
    path(r'records/<int:record_id>/', views.get_one_record, name='record-detail'),
    path(r'records/add/', views.add_record, name='add-record-post'),
    path(r'records/<int:record_id>/put/', views.put_detail, name='record-put'),
    path(r'records/<int:record_id>/delete/', views.delete_record, name='delete-record'),
    path(r'records/<int:record_id>/post/',views.add_record_to_animal, name='add-record'),

    path(r'animals/', views.get_all_animals, name='all-animals-list'),
    path(r'animals/form_animal/', views.form_animal, name='form-animal'),
    path(r'animals/delete_animal/', views.delete_animal, name='delete-animal'),
    path(r'animals/<int:animal_id>/get/', views.get_one_animal, name='get_one_animal'),
    path(r'animals/<int:animal_id>/approve_or_decline_animal/', views.approve_or_decline_animal, name='approve_or_decline_animal'),
    path(r'animals/change_animal/', views.change_animal, name='change_animal'),
    path(r'animals/update_animal_async/', views.update_animal_async, name='update_animal_async'),

    path(r'links/delete_animal_record/<int:record_id>/', views.delete_animal_record, name='delete_animal_record'),
    path(r'links/change_desc/<int:record_id>/', views.change_desc, name='change_desc'),

    path(r'account/login/', views.authorize, name='authorize'),
    path(r'account/logout/', views.logout_view, name='logout_view'),
    path(r'account/create/', views.create_account, name='create_account'),
    
    path('admin/', admin.site.urls),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
