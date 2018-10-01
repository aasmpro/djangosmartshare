from django.http import HttpResponse
from os.path import isfile, getsize
from os import listdir, mkdir, system, stat
from wsgiref.util import FileWrapper
import tempfile
import shutil


def find_deepest_location(locations, address):
    location = None
    for lo in locations:
        if str(address).__contains__(str(lo.path)):
            if location:
                if len(str(location.path)) < len(str(lo.path)):
                    location = lo
            else:
                location = lo
    return location


def handle_delete(address, data_type):
    try:
        system("rm -rf {}".format(address))
    except:
        pass


def handle_make_file(address, content):
    try:
        with open(address, 'w+') as file:
            file.write(content)
    except:
        pass


def handle_make_dir(address):
    try:
        mkdir(address)
    except:
        pass


def handle_uploaded_file(f, address):
    with open(address, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def send_file(address):
    filename = address
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={}'.format(address.split('/')[-1].replace(' ', '-'))
    response['Content-Length'] = getsize(filename)
    return response


def send_zipfile(address, data_type):
    formats = {
        'tar.gz': 'gztar',
        'tar.bz2': 'bztar',
        'zip': 'zip',
        'tar': 'tar',
    }
    tempdir = tempfile.mkdtemp()

    # archive = zipfile.ZipFile('{}/temp.zip'.format(tmpdir), 'w', zipfile.ZIP_DEFLATED)
    # for root, dirs, files in walk(address):
    #     for file in files:
    #         archive.write(join(root, file))
    # archive.close()

    shutil.make_archive('{}/temp'.format(tempdir), formats[data_type], address)

    wrapper = FileWrapper(open('{}/temp.{}'.format(tempdir, data_type), 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={}.{}'.format(address.replace(' ', '_')[1:-1], data_type)
    response['Content-Length'] = getsize('{}/temp.{}'.format(tempdir, data_type))
    shutil.rmtree(tempdir)
    return response


def get_content(path, s_files, s_dirs, h_files, h_dirs):
    path = '{}/'.format(path) if path[-1] != '/' else str(path)
    dirs = []
    files = []
    try:
        for ld in listdir(path):
            if isfile('{}{}'.format(path, ld)) and s_files:
                if ld.startswith('.'):
                    if h_files:
                        files.append({'name': ld, 'size': stat("{}{}".format(path, ld)).st_size})
                else:
                    files.append({'name': ld, 'size': stat("{}{}".format(path, ld)).st_size})
            elif s_dirs:
                if ld.startswith('.'):
                    if h_dirs:
                        dirs.append(ld)
                else:
                    dirs.append(ld)

    except FileNotFoundError:
        dirs = FileNotFoundError
        files = FileNotFoundError
        return dirs, files

    except NotADirectoryError:
        dirs = NotADirectoryError
        files = NotADirectoryError
        return dirs, files

    return sorted(dirs), files
