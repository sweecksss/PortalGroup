from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import CustomUser
from .models import Vote, Voting, VotingOption


class VotingTests(TestCase):
    def setUp(self):
        self.author = CustomUser.objects.create_user('moderator', password='testpass', role='moderator')
        self.user = CustomUser.objects.create_user('student', password='testpass')
        self.voting = Voting.objects.create(title='Обрати дату', author=self.author)
        self.first_option = VotingOption.objects.create(voting=self.voting, text='Понеділок')
        self.second_option = VotingOption.objects.create(voting=self.voting, text='Вівторок')

    def test_authenticated_user_can_vote_once_and_change_vote(self):
        self.client.force_login(self.user)
        url = reverse('votings:vote', args=[self.voting.pk])

        self.client.post(url, {'option': self.first_option.pk})
        self.client.post(url, {'option': self.second_option.pk})

        self.assertEqual(Vote.objects.filter(voting=self.voting, user=self.user).count(), 1)
        self.assertEqual(Vote.objects.get(voting=self.voting, user=self.user).option, self.second_option)

    def test_regular_user_cannot_create_voting(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('votings:create'))

        self.assertEqual(response.status_code, 302)
