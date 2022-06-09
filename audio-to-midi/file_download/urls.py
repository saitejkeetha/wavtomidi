from django.urls import path, re_path
from . import views

# namespace
app_name = 'file_download'

urlpatterns = [

    re_path(r'^download/(?P<file_path>.*)/$', views.file_response_download, name='file_download'),
    re_path(r'^convert/(?P<file_path>.*)/$', views.file_convert_download, name='file_convert'),
    re_path(r'^delete_midi/(?P<file_path>.*)/$', views.delete_midi_file, name='delete_midi_file'),

]
