from django import template
from share.defenitions import readable_size
from os import stat

register = template.Library()


@register.simple_tag
def file_size(address, file):
    return readable_size(stat("{}{}".format(address, file)).st_size, 'Byte')
