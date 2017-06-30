from __future__ import unicode_literals

from django.db import models
from ..login_and_registration_app.models import User
import datetime
from django.utils import timezone

# Create your models here.

class QuoteManager(models.Manager):
    def addQuoteVal(self, postData):
        context = {
            'error_message' : [],
            # 'success_message' : []
        }

        if not postData['quote'] or len(postData['quote']) < 10:
            context['error_message'].append(
                'ERROR: Quote needs to be at least 10 characters!')

        if not postData['author'] or len(postData['author']) < 3:
            context['error_message'].append(
                'ERROR: Author name needs to be at least 3 characters!')

        # try:
        if context['error_message'] == []:
            user = User.objects.get(id=postData['creator'])

            quote_q = Quote.objects.create(
                quote=postData['quote'],
                author=postData['author'],
                posted_by=user,
            )

            quote_q.save()

        return context


class Quote(models.Model):
    quote = models.TextField(blank=False, null=False)
    author = models.CharField(max_length=100)
    faves = models.ManyToManyField(User, related_name="users_fave")
    posted_by = models.ForeignKey(User, related_name="quoter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    def __str__(self):
        return str(self.author)
