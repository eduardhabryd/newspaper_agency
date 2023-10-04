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
    full_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by full name",
                "class": "form-control me-3",
                "type": "search",
                "aria-label": "Search"
            }
        ),
    )


class RedactorCreationForm(UserCreationForm):
    class Meta:
        model = Redactor
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(RedactorCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RedactorUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Your first name',
            'class': 'form-control mb-3',
        }
    ))

    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Your last name',
            'class': 'form-control mb-3',
        }
    ))

    profile_image = forms.ImageField(
        label='Profile Image',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control mt-2 mb-3',
            }),
        required=False
    )

    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter your old password',
            }
        ),
        required=False
    )

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter your new password',
            }
        ),
        required=False
    )

    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Confirm your new password',
            }
        ),
        required=False
    )

    class Meta:
        model = Redactor
        fields = ("first_name", "last_name", "profile_image")

    def clean(self):
        cleaned_data = super().clean()

        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError("The old password is incorrect.")

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("The new passwords do not match.")
            elif old_password == new_password1:
                raise forms.ValidationError("The new password cannot be the same as the old password.")

        return cleaned_data

    def save(self, commit=True):
        user = super(RedactorUpdateForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['new_password1']:
            user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user

