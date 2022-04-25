from itertools import chain

from django.http import Http404
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from . import forms, models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    tickets_and_reviews = sorted(chain(tickets, reviews), key=lambda instance: instance.time_created, reverse=True)
    return render(request,
                  template_name='reviews/home.html',
                  context={'tickets_and_reviews': tickets_and_reviews})


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
            raise Http404('Vous n\'avez pas la permission de modifier ce contenu.')
        edit_form = forms.TicketForm()
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
    ticket_form_class = forms.TicketForm
    review_form_class = forms.ReviewForm

    def get(self, request):
        ticket_form = self.ticket_form_class()
        review_form = self.review_form_class()
        return render(request, self.template_name,
                      context={'ticket_form': ticket_form, 'review_form': review_form})

    def post(self, request):
        ticket_form = self.ticket_form_class(request.POST, request.FILES)
        review_form = self.review_form_class(request.POST)
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
    form_class = forms.ReviewForm

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form = self.form_class()
        return render(request, self.template_name,
                      context={'ticket': ticket, 'form': form})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        form = self.form_class(request.POST)
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
            raise Http404('Vous n\'avez pas la permission de modifier ce contenu.')
        edit_form = forms.ReviewForm()
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
