from django import forms

from .models import Author, Chapter, Comment, Reader, Story, PairingType

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'nickname', 'criminal',
            'trackbear_profile', 'other_profile_url'
        ]


class ReaderForm(forms.ModelForm):
    font_size = forms.FloatField(widget=forms.NumberInput(attrs={"min": "0", "step": ".1"}))
    class Meta:
        model = Reader
        fields = [
            'member', 'serif', 'font_size'
        ]


class ChapterForm(forms.ModelForm):
    publishing_date = forms.DateField(
        widget = forms.SelectDateWidget(years=range(2005, 2027))
    )

    class Meta:
        model = Chapter
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class StoryForm(forms.ModelForm):
    G = "g"
    T = "t"
    E = "e"

    RATING_TYPE_CHOICES = {
        G: "Tout public",
        T: "Public averti",
        E: "Adulte",
    }

    story_date = forms.DateField(
        widget = forms.SelectDateWidget(years=range(2005, 2027))
    )
    pairing_type = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=PairingType.objects.all()
    )
    rating = forms.ChoiceField(
        widget=forms.Select,
        choices=RATING_TYPE_CHOICES,
    )

    class Meta:
        model = Story
        fields = '__all__'

    def __init__(self, *arg, **kwargs):
        super(StoryForm, self).__init__(*arg, **kwargs)
        self.fields["text_length"].initial = "SHORT"
        self.fields["rating"].initial = "t"


class StoryFilterForm(forms.Form):
    G = "g"
    T = "t"
    E = "e"

    RATING_TYPE_CHOICES = {
        G: "Tout public",
        T: "Public averti",
        E: "Adulte",
    }

    filter_pairing_types = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=PairingType.objects.all()
    )
    filter_authors = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Author.objects.all()
    )
    filter_ratings = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=RATING_TYPE_CHOICES
    )

class PairingTypeForm(forms.ModelForm):
    class Meta:
        model = PairingType
        fields = '__all__'

# FOR PUBLISHING
