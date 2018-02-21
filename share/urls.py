from django.urls import path
from .views import share, share_address, download_file, upload_file

urlpatterns = [
    path('', share),
    path('share/<path:address>', share_address),
    path('download/<path:address>:<ftype>', download_file),
    path('upload/<path:address>', upload_file)
]
