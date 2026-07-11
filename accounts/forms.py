from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Member

class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('username', 'email', 'password1', 'password2', 'birthday')

class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ('username', 'email', 'birthday')

class MemberSelfEditForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1800, 1900)) # We despise the youth
    )

    class Meta:
        model = Member
        fields = ('colour_scheme', 'title_blur', 'birthday')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.colour_scheme = self.cleaned_data['colour_scheme']
        instance.title_blur = self.cleaned_data['title_blur']
        instance.birthday = self.cleaned_data['birthday']
        if commit:
            instance.save(update_fields=['colour_scheme', 'title_blur', 'birthday'])
        return instance
