from django.views.generic import View
from django.shortcuts import render, redirect
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