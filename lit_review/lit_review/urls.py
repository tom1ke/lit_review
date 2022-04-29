"""lit_review URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
import authentication.views
import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', authentication.views.SignupPage.as_view(
        template_name='authentication/signup.html'),
         name='signup'),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('lougout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='authentication/password_change.html',),
         name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'),
    path('home/', reviews.views.home, name='home'),
    path('publications/', reviews.views.publications, name='publications'),
    path('follow/', reviews.views.FollowUser.as_view(), name='follow'),
    path('create_ticket/', reviews.views.TicketCreation.as_view(), name='create_ticket'),
    path('ticket/<int:ticket_id>/edit_ticket/', reviews.views.TicketEdit.as_view(), name='edit_ticket'),
    path('create_review/', reviews.views.ReviewNewCreation.as_view(), name='create_new_review'),
    path('ticket/<int:ticket_id>/create_reply_review/', reviews.views.ReviewReplyCreation.as_view(),
         name='create_reply_review'),
    path('review/<int:review_id>/edit_review', reviews.views.ReviewEdit.as_view(), name='edit_review'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
