from django import forms
from django.core.exceptions import ValidationError
from . import util

class NewPageForm(forms.Form):

    page_name = forms.CharField(label="", widget=forms.TextInput(attrs={"class": "search w-50 mb-3",
                                                                        'placeholder':'Enter a Page Name'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "w-50 h-50", 
                                                                    "placeholder": "Enter the page content"}))
    def clean_page_name(self):
        name = self.cleaned_data['page_name']
        filenames = util.list_entries()

        for filename in filenames:
            if filename.lower() == name.lower():
                raise ValidationError("A page with this name already exists.")
            
        return name
    
