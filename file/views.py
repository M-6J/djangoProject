from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload
from django.utils import timezone

def fileList(request):
    file_list = FileUpload.objects.order_by('-startdate')
    context = {'file_list': file_list}
    return render(request,'file/file_list.html',context)

def fileUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        file = request.FILES["file"]
        startdate = timezone.now()
        fileupload = FileUpload(
            title=title,
            file=file,
            startdate = startdate,
        )
        fileupload.save()
        return redirect('/file/filelist/')
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'file/fileupload.html', context)