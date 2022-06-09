from django.db import models
import os
import uuid

# Create your models here.
# Define user directory path


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    fName = filename.split('.')[-2]
    filename = '{}.{}'.format(fName, ext)
    return os.path.join("files", filename)


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=True)
    upload_method = models.CharField(max_length=20, verbose_name="Upload Method", null=True)
    
    def __str__(self) -> str:
        return self.file
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)