from django import forms

class LinearEquationForm(forms.Form):
    equations = forms.CharField(label='Equations', widget=forms.Textarea)