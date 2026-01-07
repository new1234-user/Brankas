from django import forms
from .models import Brankas

class BrankasForm(forms.ModelForm):
    class Meta:
        model = Brankas
        fields = ['judul', 'catatan', 'file_rahasia']

        def __init__(self, *args, **kwargs):
            super(BrankasForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({"class":"form-control", "style" : "margin-bottom:10px;width:100%;"})