from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import DateTimeField
from lit_review.settings import AUTH_USER_MODEL

class Ticket(models.Model):
    title = models.fields.CharField(max_length=128)
    description = models.fields.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    

class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(5)])
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.fields.CharField(max_length=128)
    body = models.fields.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    

class UserFollows(models.Model):
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')
    
    class Meta:
        unique_together = ('user', 'followed_user')