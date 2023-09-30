from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectMultiple

from agency.models import Newspaper, Redactor, Topic


class NewspaperCreateForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(
        attrs={
            'placeholder': 'Put your title here',
            'class': 'form-control',
            "id": "title_input"
        }
    ))

    content = forms.CharField(label='Content', widget=forms.Textarea(
        attrs={'placeholder': 'Here should be your content', 'class': 'form-control'}))

    image = forms.ImageField(
        label='Image',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }),
        required=False
    )

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

    class Meta:
        model = Newspaper
        fields = ['title', 'content', 'image', 'topic', 'publishers']


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title",
                "class": "form-control me-3",
                "type": "search",
                "aria-label": "Search"
            }
        ),
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by topic name",
                "class": "form-control me-3",
                "type": "search",
                "aria-label": "Search"
            }
        ),
    )


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username",
                "class": "form-control me-3",
                "type": "search",
                "aria-label": "Search"
            }
        ),
    )


class NewUserForm(UserCreationForm):
    class Meta:
        model = Redactor
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
