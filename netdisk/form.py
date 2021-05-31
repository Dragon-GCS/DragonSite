# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/5/6 21:51
# Edit with PyCharm

from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50,required=False)
    file = forms.FileField(required=False)