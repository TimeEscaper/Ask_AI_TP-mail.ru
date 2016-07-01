from django import forms

class UploadImgForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    psw_confirm = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    second_name = forms.CharField()
    img = forms.FileField()
