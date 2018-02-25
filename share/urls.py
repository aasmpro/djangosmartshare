from django.urls import path
from .views import share, share_address, download_file, upload_file, make_dir, make_file, delete

urlpatterns = [
    path('', share),
    path('share/<path:address>', share_address),
    path('download/<path:address>:<ftype>', download_file),
    path('upload/<path:address>', upload_file),
    path('mkdir/<path:address>', make_dir),
    path('mkfile/<path:address>', make_file),
    path('delete/<path:address>:<itype>', delete)
]
