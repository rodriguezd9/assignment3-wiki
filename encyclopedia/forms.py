from django import forms
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Enter content below in markdown", widget=forms.Textarea)

    def clean(self):
        super(NewEntryForm, self).clean()
        title = self.cleaned_data['title']
        
        if title in util.list_entries():
            raise forms.ValidationError("Entry already exists")
        
        return self.cleaned_data


class SearchForm(forms.Form):
        q = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))