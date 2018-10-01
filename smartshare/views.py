from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Location
from .utils import *
from .forms import UploadFileForm, MakeDirForm, MakeFileForm


def get_locations(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return Location.objects.filter(active_a=True)
        else:
            return Location.objects.filter(active_u=True)
    else:
        return Location.objects.filter(active_p=True)


def shared_locations(request):
    return render(request, template_name='smartshare/shared_locations.html',
                  context={'locations': get_locations(request)})


def location_detail(request, address):
    location = find_deepest_location(get_locations(request), address)
    if location:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                dirs, files = get_content(address, location.show_f_a, location.show_d_a, location.show_h_f_a,
                                          location.show_h_d_a)
            else:
                dirs, files = get_content(address, location.show_f_u, location.show_d_u, location.show_h_f_u,
                                          location.show_h_d_u)
        else:
            dirs, files = get_content(address, location.show_f_p, location.show_d_p, location.show_h_f_p,
                                      location.show_h_d_p)

        if dirs == FileNotFoundError:
            return render(request, 'smartshare/404.html')

        if dirs == NotADirectoryError:
            return render(request, 'smartshare/404.html')
        return render(request, template_name='smartshare/location_detail.html',
                      context={'location': location, 'address': address, 'dirs': dirs, 'files': files})
    return render(request, 'smartshare/404.html')


def download(request, address, data_type):
    location = find_deepest_location(get_locations(request), address)
    if location:
        if request.user.is_authenticated:
            if request.user.is_superuser and location.can_down_a:
                if isfile(address):
                    return send_file(address)
                elif listdir(address):
                    return send_zipfile(address, data_type)
            elif location.can_down_u and not request.user.is_superuser:
                if isfile(address):
                    return send_file(address)
                elif listdir(address):
                    return send_zipfile(address, data_type)
        elif location.can_down_p:
            if isfile(address):
                return send_file(address)
            elif listdir(address):
                return send_zipfile(address, data_type)
    return render(request, 'smartshare/404.html')


def upload(request, address):
    try:
        listdir(address)
    except:
        return render(request, 'smartshare/404.html')
    location = find_deepest_location(get_locations(request), address)
    if location:
        if request.user.is_authenticated:
            if request.user.is_superuser and location.can_up_a:
                if request.method == 'POST':
                    form = UploadFileForm(request.POST, request.FILES)
                    if form.is_valid():
                        handle_uploaded_file(request.FILES['file'], '{}{}'.format(address, request.FILES['file'].name))
                        return HttpResponseRedirect(reverse('location_detail', args=(address,)))
                else:
                    form = UploadFileForm()
                return render(request, 'smartshare/upload.html', {'form': form})

            elif location.can_up_u and not request.user.is_superuser:
                if request.method == 'POST':
                    form = UploadFileForm(request.POST, request.FILES)
                    if form.is_valid():
                        handle_uploaded_file(request.FILES['file'], '{}{}'.format(address, request.FILES['file'].name))
                        return HttpResponseRedirect(reverse('location_detail', args=(address,)))
                else:
                    form = UploadFileForm()
                return render(request, 'smartshare/upload.html', {'form': form})

        elif location.can_up_p:
            if request.method == 'POST':
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    handle_uploaded_file(request.FILES['file'], '{}{}'.format(address, request.FILES['file'].name))
                    return HttpResponseRedirect(reverse('location_detail', args=(address,)))
            else:
                form = UploadFileForm()
            return render(request, 'smartshare/upload.html', {'form': form})
    return render(request, 'smartshare/404.html')


def make_dir(request, address):
    try:
        listdir(address)
    except:
        return render(request, 'smartshare/404.html')
    location = find_deepest_location(get_locations(request), address)
    if location:
        if request.user.is_authenticated:
            if request.user.is_superuser and location.can_crt_a:
                if request.method == 'POST':
                    form = MakeDirForm(request.POST)
                    if form.is_valid():
                        handle_make_dir('{}{}'.format(address, form.data['name']))
                        return HttpResponseRedirect(reverse('location_detail', args=(address,)))
                else:
                    form = MakeDirForm()
                return render(request, 'smartshare/make_dir.html', {'form': form})

            elif location.can_crt_u and not request.user.is_superuser:
                if request.method == 'POST':
                    form = MakeDirForm(request.POST)
                    if form.is_valid():
                        handle_make_dir('{}{}'.format(address, form.data['name']))
                        return HttpResponseRedirect(reverse('location_detail', args=(address,)))
                else:
                    form = MakeDirForm()
                return render(request, 'smartshare/make_dir.html', {'form': form})

        elif location.can_crt_p:
            if request.method == 'POST':
                form = MakeDirForm(request.POST)
                if form.is_valid():
                    handle_make_dir('{}{}'.format(address, form.data['name']))
                    return HttpResponseRedirect(reverse('location_detail', args=(address,)))
            else:
                form = MakeDirForm()
            return render(request, 'smartshare/make_dir.html', {'form': form})
    return render(request, 'smartshare/404.html')


def make_file(request, address):
    try:
        listdir(address)
    except:
        return render(request, 'smartshare/404.html')
    location = find_deepest_location(get_locations(request), address)
    if location:
        if request.user.is_authenticated:
            if request.user.is_superuser and location.can_crt_a:
                if request.method == 'POST':
                    form = MakeFileForm(request.POST)
                    if form.is_valid():
                        handle_make_file('{}{}'.format(address, form.data['name']), form.data['content'])
                        return HttpResponseRedirect(reverse('location_detail', args=(address,)))
                else:
                    form = MakeFileForm()
                return render(request, 'smartshare/make_file.html', {'form': form})

            elif location.can_crt_u and not request.user.is_superuser:
                if request.method == 'POST':
                    form = MakeFileForm(request.POST)
                    if form.is_valid():
                        handle_make_file('{}{}'.format(address, form.data['name']), form.data['content'])
                        return HttpResponseRedirect(reverse('location_detail', args=(address,)))
                else:
                    form = MakeFileForm()
                return render(request, 'smartshare/make_file.html', {'form': form})

        elif location.can_crt_p:
            if request.method == 'POST':
                form = MakeFileForm(request.POST)
                if form.is_valid():
                    handle_make_file('{}{}'.format(address, form.data['name']), form.data['content'])
                    return HttpResponseRedirect(reverse('location_detail', args=(address,)))
            else:
                form = MakeFileForm()
            return render(request, 'smartshare/make_file.html', {'form': form})
    return render(request, 'smartshare/404.html')


def delete(request, address, data_type):
    location = find_deepest_location(get_locations(request), address)
    if location:
        if request.user.is_authenticated:
            if request.user.is_superuser and location.can_del_a:
                if request.method == 'POST':
                    if 'Delete' in request.POST:
                        handle_delete(address, data_type)
                    address = address[:address[0:-1].rfind('/') + 1]
                    return HttpResponseRedirect(reverse('location_detail', args=(address,)))
                return render(request, 'smartshare/delete.html', {'address': address, 'data_type': data_type})

            elif location.can_del_u and not request.user.is_superuser:
                if request.method == 'POST':
                    form = MakeFileForm(request.POST)
                    if form.is_valid():
                        handle_delete(address, data_type)
                        return HttpResponseRedirect(reverse('location_detail', args=(address,)))
                else:
                    form = MakeFileForm()
                return render(request, 'smartshare/delete.html', {'form': form})

        elif location.can_del_p:
            if request.method == 'POST':
                form = MakeFileForm(request.POST)
                if form.is_valid():
                    handle_delete(address, data_type)
                    return HttpResponseRedirect(reverse('location_detail', args=(address,)))
            else:
                form = MakeFileForm()
            return render(request, 'smartshare/delete.html', {'form': form})
    return render(request, 'smartshare/404.html')
