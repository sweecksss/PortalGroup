from django.conf import settings
from django.db import models


class Voting(models.Model):
    title = models.CharField('Питання', max_length=255)
    description = models.TextField('Опис', blank=True)
    is_active = models.BooleanField('Активне', default=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='votings',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class VotingOption(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='options')
    text = models.CharField('Варіант відповіді', max_length=255)

    def __str__(self):
        return self.text


class Vote(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(VotingOption, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('voting', 'user'), name='one_vote_per_user'),
        ]
