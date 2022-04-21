from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from . import forms, models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request,
                  template_name='reviews/home.html',
                  context={'tickets': tickets})


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
        blog = get_object_or_404(models.Ticket, id=ticket_id)
        edit_form = forms.TicketForm()
        delete_form = forms.DeleteTicketForm()
        return render(request, self.template_name,
                      context={'edit_form': edit_form, 'delete_form': delete_form})
    
    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        edit_form = forms.TicketForm(instance=ticket)
        delete_form = forms.DeleteTicketForm()
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
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

