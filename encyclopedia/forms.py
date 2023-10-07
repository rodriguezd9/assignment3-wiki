from django import forms
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

    def clean(self):
        #WRONG: super(NewTaskForm, self.clean())
        super(NewEntryForm, self).clean()
        title = self.cleaned_data['title']
        content = self.cleaned_data['content']
        
        if title in util.list_entries():
            raise forms.ValidationError("Entry already exists")
        
        return self.cleaned_data


