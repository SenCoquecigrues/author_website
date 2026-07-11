from django import forms

from .models import ExchangeParticipant, Prompt


class ExchangeParticipantForm(forms.ModelForm):
    class Meta:
        model = ExchangeParticipant
        fields = ["member", "likes", "dislikes"]


class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ["body", "pairing_type"]
