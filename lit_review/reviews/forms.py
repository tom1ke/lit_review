from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        labels = {'title': 'Titre & auteur', 'description': 'Description'}


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        labels = {'headline': 'Titre de la réponse', 'rating': 'Note', 'body': 'Critique'}


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
        labels = {'followed_user': 'Utilisateur'}
