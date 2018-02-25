from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Location
from os.path import isfile
from .defenitions import *
from .forms import UploadFileForm, MakeDirForm, MakeFileForm


def share(request):
    locations = Location.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            locations = locations.filter(active_a=True)
        else:
            locations = locations.filter(active_u=True)
    else:
        locations = locations.filter(active_p=True)
    return render(request, template_name='share.html', context={'locations': locations})


def share_address(request, address):
    address = "/{}".format(address)
    locations = Location.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            locations = locations.filter(active_a=True)
        else:
            locations = locations.filter(active_u=True)
    else:
        locations = locations.filter(active_p=True)
    lo = None
    for location in locations:
        if str(address).__contains__(str(location.path)):
            if lo:
                if len(str(lo.path)) < len(str(location.path)):
                    lo = location
            else:
                lo = location

    if lo:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                dirs, files = get_content(address, lo.show_f_a, lo.show_d_a, lo.show_h_f_a, lo.show_h_d_a)
            else:
                dirs, files = get_content(address, lo.show_f_u, lo.show_d_u, lo.show_h_f_u, lo.show_h_d_u)
        else:
            dirs, files = get_content(address, lo.show_f_p, lo.show_d_p, lo.show_h_f_p, lo.show_h_d_p)

        if dirs == FileNotFoundError:
            return render(request, '404.html')

        if dirs == NotADirectoryError:
            # file_stat = stat(address)
            # file = {
            #     'name': address.split('/')[-1],
            #     'type': address.split('/')[-1].split('.')[-1],
            #     'byte_size': file_stat.st_size,
            #     'readable_size': readable_size(file_stat.st_size, 'Byte')
            # }
            # return render(request, template_name='files.html', context={'address': address, 'file': file})
            return render(request, '404.html')
        return render(request, template_name='dirs.html',
                      context={'location': lo, 'address': address, 'dirs': dirs, 'files': files})
    return render(request, '404.html')


def download_file(request, address, ftype):
    address = "/{}".format(address)
    locations = Location.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            locations = locations.filter(active_a=True)
        else:
            locations = locations.filter(active_u=True)
    else:
        locations = locations.filter(active_p=True)
    lo = None
    for location in locations:
        if str(address).__contains__(str(location.path)):
            if lo:
                if len(str(lo.path)) < len(str(location.path)):
                    lo = location
            else:
                lo = location

    if lo:
        if request.user.is_authenticated:
            if request.user.is_superuser and lo.can_down_a:
                if isfile(address):
                    return send_file(address)
                elif listdir(address):
                    return send_zipfile(address, ftype)
            elif lo.can_down_u and not request.user.is_superuser:
                if isfile(address):
                    return send_file(address)
                elif listdir(address):
                    return send_zipfile(address, ftype)
        elif lo.can_down_p:
            if isfile(address):
                return send_file(address)
            elif listdir(address):
                return send_zipfile(address, ftype)
    return render(request, '404.html')


def upload_file(request, address):
    address = "/{}".format(address)
    try:
        listdir(address)
    except:
        return render(request, '404.html')
    locations = Location.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            locations = locations.filter(active_a=True)
        else:
            locations = locations.filter(active_u=True)
    else:
        locations = locations.filter(active_p=True)
    lo = None
    for location in locations:
        if str(address).__contains__(str(location.path)):
            if lo:
                if len(str(lo.path)) < len(str(location.path)):
                    lo = location
            else:
                lo = location
    if lo:
        if request.user.is_authenticated:
            if request.user.is_superuser and lo.can_up_a:
                if request.method == 'POST':
                    form = UploadFileForm(request.POST, request.FILES)
                    if form.is_valid():
                        handle_uploaded_file(request.FILES['file'], '{}{}'.format(address, request.FILES['file'].name))
                        return HttpResponseRedirect('/share{}'.format(address))
                else:
                    form = UploadFileForm()
                return render(request, 'upload.html', {'form': form})

            elif lo.can_up_u and not request.user.is_superuser:
                if request.method == 'POST':
                    form = UploadFileForm(request.POST, request.FILES)
                    if form.is_valid():
                        handle_uploaded_file(request.FILES['file'], '{}{}'.format(address, request.FILES['file'].name))
                        return HttpResponseRedirect('/share{}'.format(address))
                else:
                    form = UploadFileForm()
                return render(request, 'upload.html', {'form': form})

        elif lo.can_up_p:
            if request.method == 'POST':
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    handle_uploaded_file(request.FILES['file'], '{}{}'.format(address, request.FILES['file'].name))
                    return HttpResponseRedirect('/share{}'.format(address))
            else:
                form = UploadFileForm()
            return render(request, 'upload.html', {'form': form})
    return render(request, '404.html')


def make_dir(request, address):
    address = "/{}".format(address)
    try:
        listdir(address)
    except:
        return render(request, '404.html')
    locations = Location.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            locations = locations.filter(active_a=True)
        else:
            locations = locations.filter(active_u=True)
    else:
        locations = locations.filter(active_p=True)
    lo = None
    for location in locations:
        if str(address).__contains__(str(location.path)):
            if lo:
                if len(str(lo.path)) < len(str(location.path)):
                    lo = location
            else:
                lo = location
    if lo:
        if request.user.is_authenticated:
            if request.user.is_superuser and lo.can_crt_a:
                if request.method == 'POST':
                    form = MakeDirForm(request.POST)
                    if form.is_valid():
                        handle_make_dir('{}{}'.format(address, form.data['name']))
                        return HttpResponseRedirect('/share{}'.format(address))
                else:
                    form = MakeDirForm()
                return render(request, 'make_dir.html', {'form': form})

            elif lo.can_crt_u and not request.user.is_superuser:
                if request.method == 'POST':
                    form = MakeDirForm(request.POST)
                    if form.is_valid():
                        handle_make_dir('{}{}'.format(address, form.data['name']))
                        return HttpResponseRedirect('/share{}'.format(address))
                else:
                    form = MakeDirForm()
                return render(request, 'make_dir.html', {'form': form})

        elif lo.can_crt_p:
            if request.method == 'POST':
                form = MakeDirForm(request.POST)
                if form.is_valid():
                    handle_make_dir('{}{}'.format(address, form.data['name']))
                    return HttpResponseRedirect('/share{}'.format(address))
            else:
                form = MakeDirForm()
            return render(request, 'make_dir.html', {'form': form})
    return render(request, '404.html')


def make_file(request, address):
    address = "/{}".format(address)
    try:
        listdir(address)
    except:
        return render(request, '404.html')
    locations = Location.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            locations = locations.filter(active_a=True)
        else:
            locations = locations.filter(active_u=True)
    else:
        locations = locations.filter(active_p=True)
    lo = None
    for location in locations:
        if str(address).__contains__(str(location.path)):
            if lo:
                if len(str(lo.path)) < len(str(location.path)):
                    lo = location
            else:
                lo = location
    if lo:
        if request.user.is_authenticated:
            if request.user.is_superuser and lo.can_crt_a:
                if request.method == 'POST':
                    form = MakeFileForm(request.POST)
                    if form.is_valid():
                        handle_make_file('{}{}'.format(address, form.data['name']), form.data['content'])
                        return HttpResponseRedirect('/share{}'.format(address))
                else:
                    form = MakeFileForm()
                return render(request, 'make_file.html', {'form': form})

            elif lo.can_crt_u and not request.user.is_superuser:
                if request.method == 'POST':
                    form = MakeFileForm(request.POST)
                    if form.is_valid():
                        handle_make_file('{}{}'.format(address, form.data['name']), form.data['content'])
                        return HttpResponseRedirect('/share{}'.format(address))
                else:
                    form = MakeFileForm()
                return render(request, 'make_file.html', {'form': form})

        elif lo.can_crt_p:
            if request.method == 'POST':
                form = MakeFileForm(request.POST)
                if form.is_valid():
                    handle_make_file('{}{}'.format(address, form.data['name']), form.data['content'])
                    return HttpResponseRedirect('/share{}'.format(address))
            else:
                form = MakeFileForm()
            return render(request, 'make_file.html', {'form': form})
    return render(request, '404.html')


def delete(request, address, itype):
    address = "/{}".format(address)
    locations = Location.objects.all()
    if request.user.is_authenticated:
        if request.user.is_superuser:
            locations = locations.filter(active_a=True)
        else:
            locations = locations.filter(active_u=True)
    else:
        locations = locations.filter(active_p=True)
    lo = None
    for location in locations:
        if str(address).__contains__(str(location.path)):
            if lo:
                if len(str(lo.path)) < len(str(location.path)):
                    lo = location
            else:
                lo = location
    if lo:
        if request.user.is_authenticated:
            if request.user.is_superuser and lo.can_del_a:
                if request.method == 'POST':
                    if 'Delete' in request.POST:
                        handle_delete(address, itype)
                    address = address[:address[0:-1].rfind('/')+1]
                    return HttpResponseRedirect('/share{}'.format(address))
                return render(request, 'delete.html', {'address': address, 'itype': itype})

            elif lo.can_del_u and not request.user.is_superuser:
                if request.method == 'POST':
                    form = MakeFileForm(request.POST)
                    if form.is_valid():
                        handle_delete(address, itype)
                        return HttpResponseRedirect('/share{}'.format(address))
                else:
                    form = MakeFileForm()
                return render(request, 'delete.html', {'form': form})

        elif lo.can_del_p:
            if request.method == 'POST':
                form = MakeFileForm(request.POST)
                if form.is_valid():
                    handle_delete(address, itype)
                    return HttpResponseRedirect('/share{}'.format(address))
            else:
                form = MakeFileForm()
            return render(request, 'delete.html', {'form': form})
    return render(request, '404.html')
