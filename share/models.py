from django.db import models
from django.core.exceptions import ValidationError
from os import listdir


class Location(models.Model):
    # location = models.FilePathField(path='/home/', recursive=True, allow_folders=True, allow_files=False)
    path = models.CharField(max_length=300)
    am_choices = (
        ('R', 'Read'),
        ('W', 'Write'),
        ('RW', 'Read-Write')
    )
    access_mode = models.CharField(max_length=2, choices=am_choices, default='R')
    show_hidden_files = models.BooleanField(default=False)
    show_hidden_dirs = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.path

    def clean(self):
        try:
            listdir(self.path)
            if self.path[-1] != '/':
                self.path += '/'
        except FileNotFoundError:
            raise ValidationError("'{}' is not a real path on server.".format(self.path))

        except NotADirectoryError:
            raise ValidationError("'{}' is not a directory.".format(self.path))
