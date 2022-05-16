from django import forms
from django.contrib.auth import get_user_model


from . import models

User = get_user_model()


class CustomModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomModelForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].label = ''


class TicketForm(CustomModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre & auteur', 'description': 'Description'}


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(CustomModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    CHOICES = (
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    )

    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='Note')

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre de la réponse', 'rating': 'Note', 'body': 'Critique'}


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUserForm(forms.Form):
    follow_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    follow = forms.CharField(max_length=100, label='Suivre')


class UnfollowUserForm(forms.Form):
    unfollow_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
