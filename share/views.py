from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Location
from os import stat
from os.path import isfile
from .defenitions import *
from .forms import UploadFileForm


def share(request):
    locations = Location.objects.all()
    return render(request, template_name='share.html', context={'locations': locations})


def share_address(request, address):
    address = "/{}".format(address)
    locations = Location.objects.all()
    lo = None
    for location in locations:
        if str(address).__contains__(str(location.path)):
            if lo:
                if len(str(lo.path)) < len(str(location.path)):
                    lo = location
            else:
                lo = location

    if lo:
        dirs, files = get_content(address, lo.show_hidden_dirs, lo.show_hidden_files)
        if dirs == FileNotFoundError:
            return render(request, template_name='dirs.html', context={'address': None})
        if dirs == NotADirectoryError:
            file_stat = stat(address)
            file = {
                'name': address.split('/')[-1],
                'type': address.split('/')[-1].split('.')[-1],
                'byte_size': file_stat.st_size,
                'readable_size': readable_size(file_stat.st_size, 'Byte')
            }
            return render(request, template_name='files.html',
                          context={'address': address, 'file': file})
        return render(request, template_name='dirs.html',
                      context={'location': lo, 'address': address, 'dirs': dirs, 'files': files})
    return render(request, template_name='dirs.html', context={'address': None})


def download_file(request, address, ftype):
    address = "/{}".format(address)
    if isfile(address):
        return send_file(address)
    else:
        return send_zipfile(address, ftype)


def upload_file(request, address):
    address = "/{}".format(address)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], '{}{}'.format(address, request.FILES['file'].name))
            return HttpResponseRedirect('/share{}'.format(address))
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
