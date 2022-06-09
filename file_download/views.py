import os
from django.http import HttpResponse, Http404, StreamingHttpResponse, FileResponse

from subprocess import Popen
import threading
import time
from file_upload.views import *
from setuptools import Command
# Create your views here.
# Case 1: simple file download, very bad
# Reason 1: loading file to memory and consuming memory
# Can download all files, including raw python .py codes


def file_download(request, file_path):
    # do something...
    with open(file_path) as f:
        c = f.read()
    return HttpResponse(c)


# Case 2 Use HttpResponse to download a small file
# Good for txt, not suitable for big binary files
def media_file_download(request, file_path):
    with open(file_path, 'rb') as f:
        try:
            response = HttpResponse(f)
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        except Exception:
            raise Http404


# Case 3 Use StreamingHttpResponse to download a large file
# Good for streaming large binary files, ie. CSV files
# Do not support python file "with" handle. Consumes response time
def stream_http_download(request, file_path):
    try:
        response = StreamingHttpResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404


# Case 4 Use FileResponse to download a large file
# It streams the file out in small chunks
# It is a subclass of StreamingHttpResponse
# Use @login_required to limit download to logined users
def file_response_download1(request, file_path):
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    except Exception:
        raise Http404


# Case 5 Limit file download type - recommended
def file_response_download(request, file_path):
    ext = os.path.basename(file_path).split('.')[-1].lower()
    # cannot be used to download py, db and sqlite3 files.
    if ext not in ['py', 'db',  'sqlite3']:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response
    else:
        raise Http404
    

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      #print ("Starting " + self.name)
      # Get lock to synchronize threads
      threadLock.acquire()
      converter(self.name)
      # Free lock to release next thread
      threadLock.release()

threadLock = threading.Lock()
threads = []


def converter(file_path):
    file_name = os.path.basename(file_path).split('.')[-2]
    infile=str(file_path)
    output = "--output " +file_name+".midi"
    cmd='cmd /k "audio-to-midi --no-progress %s %s"' % (output, infile )
    os.system(cmd) 


def file_convert_download(request, file_path):
    thread1 = myThread(1, file_path, 1)
    thread1.start()
    time.sleep(5)
    #ext = os.path.basename(file_path).split('.')[-1].lower()
    file_name = os.path.basename(file_path).split('.')[-2]
    newFilePath="./" + file_name + ".midi"  
    ext = os.path.basename(newFilePath).split('.')[-1].lower()  
    # cannot be used to download py, db and sqlite3 files.
    if os.path.exists(newFilePath):
        with open(newFilePath, 'rb') as fh:
            file_content=fh.read()
            #os.remove(newFilePath)
            response = HttpResponse(file_content, content_type="application/midi")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(newFilePath)
            return response
    raise Http404
    #return redirect('/')
    

def delete_midi_file(request, file_path):
    file_name = os.path.basename(file_path).split('.')[-2]
    newFilePath="./" + file_name + ".midi"  
    ext = os.path.basename(newFilePath).split('.')[-1].lower()  
    # cannot be used to download py, db and sqlite3 files.
    if os.path.exists(newFilePath):
        p = Popen("rm %s" % newFilePath, shell=True)
        return redirect("/file/")
    raise Http404
    