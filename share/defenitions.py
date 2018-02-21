from django.http import HttpResponse
from os.path import isfile, getsize, join
from os import listdir, walk
from wsgiref.util import FileWrapper
import tempfile, zipfile
import shutil


def handle_uploaded_file(f, address):
    with open(address, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def send_file(address):
    filename = address
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={}'.format(address.split('/')[-1])
    response['Content-Length'] = getsize(filename)
    return response


def send_zipfile(address, ftype):
    maftype = {
        'tar.gz': 'gztar',
        'tar.bz2': 'bztar',
        'zip': 'zip',
        'tar': 'tar',
    }
    tmpdir = tempfile.mkdtemp()

    # archive = zipfile.ZipFile('{}/temp.zip'.format(tmpdir), 'w', zipfile.ZIP_DEFLATED)
    # for root, dirs, files in walk(address):
    #     for file in files:
    #         archive.write(join(root, file))
    # archive.close()

    shutil.make_archive('{}/temp'.format(tmpdir), maftype[ftype], address)

    wrapper = FileWrapper(open('{}/temp.{}'.format(tmpdir, ftype), 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={}.{}'.format(address, ftype)
    response['Content-Length'] = getsize('{}/temp.{}'.format(tmpdir, ftype))
    shutil.rmtree(tmpdir)
    return response


def readable_size(size, label):
    size_replace = {
        'Byte': 'KB',
        'KB': 'MB',
        'MB': 'GB'
    }
    if size >= 1000 and label != 'GB':
        size /= 1000
        label = size_replace[label]
        return readable_size(size, label)

    if type(size) is int:
        return '{} {label}'.format(size, label=label)

    else:
        return '{0:.2f} {label}'.format(round(size, 2), label=label)


def get_content(path, hidden_dirs=False, hidden_files=False):
    path = '{}/'.format(path) if path[-1] != '/' else str(path)
    dirs = []
    files = []
    try:
        for ld in listdir(path):
            if isfile('{}{}'.format(path, ld)):
                if ld.startswith('.'):
                    if hidden_files:
                        files.append(ld)
                else:
                    files.append(ld)
            else:
                if ld.startswith('.'):
                    if hidden_dirs:
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

    return sorted(dirs), sorted(files)
