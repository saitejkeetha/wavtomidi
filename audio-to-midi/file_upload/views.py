from django.shortcuts import render, redirect
from .models import File
from .forms import FileUploadForm, FileUploadModelForm
import os
import uuid
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat
from django.core import management
from audio_to_midi.main import main

from file_download.views import *

import threading
# Create your views here.


# Show file list
def file_list(request):
    files = File.objects.all().order_by("-id")
    return render(request, 'file_upload/file_list.html', {'files': files})


# Regular file upload without using ModelForm
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get("file")
            new_file = File()
            new_file.file = handle_uploaded_file(raw_file)
            new_file.upload_method = upload_method
            new_file.save()
            return redirect("/file/")
    else:
        form = FileUploadForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload files with Regular Form'})


# Delete file
def delete_file(request, pk):
    if request.method == "POST":
        file=File.objects.get(id=pk)
        file_path=file.file.url
        file.delete()
        file_name = os.path.basename(file_path).split('.')[-2]
        newFilePath="./" + file_name + ".midi"   
        # cannot be used to download py, db and sqlite3 files.
        if os.path.exists(newFilePath):
            #p = Popen("rm %s" % newFilePath, shell=True)
            os.remove(newFilePath)
    return redirect('/')
    

def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    fName = file.name.split('.')[-1]
    #file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    file_name = '{}.{}'.format(fName, ext)
    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path


# Upload File with ModelForm
def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/file/")
    else:
        form = FileUploadModelForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload files with ModelForm'})


# Upload File with ModelForm
def ajax_form_upload(request):
    form = FileUploadModelForm()
    return render(request, 'file_upload/ajax_upload_form.html', {'form': form,
                                                            'heading': 'File Upload with AJAX'})


# handling AJAX requests
def ajax_upload(request):
    if request.method == "POST":
        # 1. Regular save method
        # upload_method = request.POST.get("upload_method")
        # raw_file = request.FILES.get("file")
        # new_file = File()
        # new_file.file = handle_uploaded_file(raw_file)
        # new_file.upload_method = upload_method
        # new_file.save()

        # 2. Use ModelForm als ok.
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # Obtain the latest file list
            files = File.objects.all().order_by('-id')
            data = []
            for file in files:
                data.append({
                    "url": file.file.url,
                    "size": filesizeformat(file.file.size),
                    "upload_method": file.upload_method,
                    })
            return JsonResponse(data, safe=False)
        else:
            data = {'error_msg': "Only jpg, pdf and xlsx files are allowed."}
            return JsonResponse(data)
    return JsonResponse({'error_msg': 'only POST method accpeted.'})
