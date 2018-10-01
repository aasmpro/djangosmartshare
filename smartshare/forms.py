from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class MakeDirForm(forms.Form):
    name = forms.CharField(max_length=300)


class MakeFileForm(forms.Form):
    name = forms.CharField(max_length=300)
    content = forms.CharField(widget=forms.Textarea, required=False)
