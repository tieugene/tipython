"""
core.forms
"""

from django import forms


class FileSeqItemAddForm(forms.Form):
    file = forms.FileField(label='File', required=False)
