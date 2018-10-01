from django.db import models
from django.core.exceptions import ValidationError
from os import listdir


class Location(models.Model):
    path = models.CharField(max_length=300)

    # for Public
    active_p = models.BooleanField(default=True, verbose_name="Active")
    show_f_p = models.BooleanField(default=True, verbose_name="Show Files")
    show_d_p = models.BooleanField(default=True, verbose_name="Show Directories")
    show_h_f_p = models.BooleanField(default=False, verbose_name="Show Hidden Files")
    show_h_d_p = models.BooleanField(default=False, verbose_name="Show Hidden Directories")
    can_down_p = models.BooleanField(default=False, verbose_name="Can Download")
    can_up_p = models.BooleanField(default=False, verbose_name="Can Upload")
    can_del_p = models.BooleanField(default=False, verbose_name="Can Delete")
    can_crt_p = models.BooleanField(default=False, verbose_name="Can Create")
    can_run_p = models.BooleanField(default=False, verbose_name="Can Run Command")

    # for Users
    active_u = models.BooleanField(default=True, verbose_name="Active")
    show_f_u = models.BooleanField(default=True, verbose_name="Show Files")
    show_d_u = models.BooleanField(default=True, verbose_name="Show Directories")
    show_h_f_u = models.BooleanField(default=False, verbose_name="Show Hidden Files")
    show_h_d_u = models.BooleanField(default=False, verbose_name="Show Hidden Directories")
    can_down_u = models.BooleanField(default=True, verbose_name="Can Download")
    can_up_u = models.BooleanField(default=True, verbose_name="Can Upload")
    can_del_u = models.BooleanField(default=False, verbose_name="Can Delete")
    can_crt_u = models.BooleanField(default=True, verbose_name="Can Create")
    can_run_u = models.BooleanField(default=False, verbose_name="Can Run Command")

    # for Admins
    active_a = models.BooleanField(default=True, verbose_name="Active")
    show_f_a = models.BooleanField(default=True, verbose_name="Show Files")
    show_d_a = models.BooleanField(default=True, verbose_name="Show Directories")
    show_h_f_a = models.BooleanField(default=True, verbose_name="Show Hidden Files")
    show_h_d_a = models.BooleanField(default=True, verbose_name="Show Hidden Directories")
    can_down_a = models.BooleanField(default=True, verbose_name="Can Download")
    can_up_a = models.BooleanField(default=True, verbose_name="Can Upload")
    can_del_a = models.BooleanField(default=True, verbose_name="Can Delete")
    can_crt_a = models.BooleanField(default=True, verbose_name="Can Create")
    can_run_a = models.BooleanField(default=True, verbose_name="Can Run Command")

    def __str__(self):
        return self.path

    def clean(self):
        try:
            listdir(self.path)
            if self.path[-1] != '/':
                self.path += '/'
        except FileNotFoundError:
            raise ValidationError("'{}' is not a real path on server.".format(self.path or 'Empty'))

        except NotADirectoryError:
            raise ValidationError("'{}' is not a directory.".format(self.path or 'Empty'))
