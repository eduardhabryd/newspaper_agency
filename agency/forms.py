from django import forms
from django.forms import SelectMultiple

from agency.models import Newspaper, Redactor, Topic


class NewspaperCreateForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ['title', 'content', 'topic', 'publishers']

    title = forms.CharField(label='Title', widget=forms.TextInput(
        attrs={
            'placeholder': 'Put your title here',
            'class': 'form-control',
            "id": "title_input"
        }
    ))

    content = forms.CharField(label='Content', widget=forms.Textarea(
        attrs={'placeholder': 'Here should be your content', 'class': 'form-control'}))

    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select',
            "value": "Example placeholder"
        }),
        initial="Example placeholder",
    )

    publishers = forms.ModelMultipleChoiceField(
        queryset=Redactor.objects.all(),
        widget=SelectMultiple(attrs={
            'class': 'form-select',
            "value": "Example placeholder"
        }),
        initial="Example placeholder",
    )