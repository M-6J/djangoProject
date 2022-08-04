from django.urls import path,include
from .views import *

from django.conf import settings
from django.conf.urls.static import static
app_name = 'file'

urlpatterns = [
	path('filelist/', fileList, name="filelist"),
	path('<int:file_id>', fileDetail, name="filedetail"),
	path('<int:file_id>/modify', fileModify, name="filemodify"),
	path('<int:file_id>/delete', fileDelete, name="filedelete"),
	path('fileupload/', fileUpload, name="fileupload"),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)