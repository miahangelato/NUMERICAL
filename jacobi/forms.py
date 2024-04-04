

from django import forms

class GaussJacobiForm(forms.Form):
    equations = forms.CharField(label='Equations', widget=forms.Textarea)
    iterations = forms.IntegerField(label='Number of Iterations')
    initial_guesses = forms.CharField(label='Initial Guesses')
