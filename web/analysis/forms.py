from django import forms


class UploadFileForm(forms.Form):
    bone_type = forms.CharField(label='bone_type', max_length=50)
    file = forms.FileField()
