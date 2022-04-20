from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator


@login_required
def home(request):
    return render(request,
                  template_name='reviews/home.html',)