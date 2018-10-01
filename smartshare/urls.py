from django.urls import path
from .views import shared_locations, location_detail, download, upload, make_dir, make_file, delete

urlpatterns = [
    path('', shared_locations, name='locations'),
    path('path<path:address>', location_detail, name='location_detail'),
    path('download<path:address>:<data_type>', download, name='download'),
    path('upload<path:address>', upload, name='upload'),
    path('makedir<path:address>', make_dir, name='makedir'),
    path('makefile<path:address>', make_file, name='makefile'),
    path('delete<path:address>:<data_type>', delete, name='delete')
]
