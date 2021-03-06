from itertools import chain

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from . import forms, models


@login_required
def home(request):
    tickets = models.Ticket.objects.filter(user_id=request.user.id)
    reviews = models.Review.objects.filter(
        Q(user_id=request.user.id) | Q(ticket__in=tickets))
    followings = models.UserFollows.objects.filter(user=request.user)
    for following in followings:
        tickets = chain(tickets, models.Ticket.objects.filter(user_id=following.followed_user))
        reviews = chain(reviews, models.Review.objects.filter(user_id=following.followed_user))
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)
    paginator = Paginator(tickets_and_reviews, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  template_name='reviews/home.html',
                  context={'page': page})


@login_required
def publications(request):
    tickets = models.Ticket.objects.filter(user_id=request.user.id)
    reviews = models.Review.objects.filter(user_id=request.user.id)
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)
    paginator = Paginator(tickets_and_reviews, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  template_name='reviews/publications.html',
                  context={'page': page})


@method_decorator(login_required, name='dispatch')
class TicketCreation(View):
    template_name = 'reviews/create_ticket.html'
    form_class = forms.TicketForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


@method_decorator(login_required, name='dispatch')
class TicketEdit(View):
    template_name = 'reviews/edit_ticket.html'

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        if ticket.user != request.user:
            raise HttpResponseNotAllowed('Vous n\'avez pas la permission de modifier ce contenu.')
        edit_form = forms.TicketForm(instance=ticket)
        delete_form = forms.DeleteTicketForm()
        return render(request, self.template_name,
                      context={'edit_form': edit_form, 'delete_form': delete_form})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        edit_form = forms.TicketForm(instance=ticket)
        delete_form = forms.DeleteTicketForm()
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
        return render(request, self.template_name,
                      context={'edit_form': edit_form, 'delete_form': delete_form})


@method_decorator(login_required, name='dispatch')
class ReviewNewCreation(View):
    template_name = 'reviews/create_new_review.html'

    def get(self, request):
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()
        return render(request, self.template_name,
                      context={'ticket_form': ticket_form, 'review_form': review_form})

    def post(self, request):
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
        return render(request, self.template_name,
                      context={'ticket_form': ticket_form, 'review_form': review_form})


@method_decorator(login_required, name='dispatch')
class ReviewReplyCreation(View):
    template_name = 'reviews/create_reply_review.html'

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form = forms.ReviewForm()
        return render(request, self.template_name,
                      context={'ticket': ticket, 'form': form})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
        return render(request, self.template_name,
                      context={'ticket': ticket, 'form': form})


@method_decorator(login_required, name='dispatch')
class ReviewEdit(View):
    template_name = 'reviews/edit_review.html'

    def get(self, request, review_id):
        review = get_object_or_404(models.Review, id=review_id)
        if review.user != request.user:
            raise HttpResponseNotAllowed('Vous n\'avez pas la permission de modifier ce contenu.')
        edit_form = forms.ReviewForm(instance=review)
        delete_form = forms.DeleteReviewForm()
        return render(request, self.template_name,
                      context={'edit_form': edit_form, 'delete_form': delete_form})

    def post(self, request, review_id):
        review = get_object_or_404(models.Review, id=review_id)
        edit_form = forms.ReviewForm(instance=review)
        delete_form = forms.DeleteReviewForm()
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('home')
        return render(request, self.template_name,
                      context={'edit_form': edit_form, 'delete_form': delete_form})


@method_decorator(login_required, name='dispatch')
class FollowUser(View):
    template_name = 'reviews/follow_user.html'

    def get(self, request):
        follow_form = forms.FollowUserForm()
        unfollow_form = forms.UnfollowUserForm()
        followed_users = models.UserFollows.objects.filter(user_id=request.user.id)
        followers = models.UserFollows.objects.filter(followed_user_id=request.user.id)
        return render(request, self.template_name,
                      context={'follow_form': follow_form,
                               'unfollow_form': unfollow_form,
                               'followed_users': followed_users,
                               'followers': followers})

    def post(self, request):
        follow_form = forms.FollowUserForm(request.POST)
        unfollow_form = forms.UnfollowUserForm(request.POST)
        following = models.UserFollows()
        user_model = get_user_model()
        users = user_model.objects.all()
        if 'follow_user' in request.POST and follow_form.is_valid():
            follow = follow_form.cleaned_data['follow']
            if follow == request.user.username:
                raise ValidationError('Vous ne pouvez pas vous abonner ?? vous-m??me.')
            usernames = [user.username for user in users]
            if follow not in usernames:
                raise ValidationError('Cet utilisateur n\'existe pas.')
            for user in users:
                try:
                    if follow == user.username:
                        following.user = request.user
                        following.followed_user = user
                        following.save()
                except IntegrityError as error:
                    raise ValidationError('Vous suivez d??j?? cet utilisateur.') from error
            return redirect('follow')
        if 'unfollow_user' in request.POST and unfollow_form.is_valid():
            unfollow = request.POST['unfollow']
            user_to_unfollow = user_model.objects.get(username=unfollow)
            sub = models.UserFollows.objects.get(user_id=request.user.id, followed_user_id=user_to_unfollow.id)
            sub.delete()
            return redirect('follow')
        return render(request, self.template_name,
                      context={'follow_form': follow_form, 'unfollow_form': unfollow_form})
