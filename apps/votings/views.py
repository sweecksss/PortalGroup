from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import moderator_required
from .forms import VotingForm
from .models import Vote, Voting, VotingOption


def voting_list(request):
    votings = Voting.objects.prefetch_related('options').select_related('author')
    return render(request, 'votings/list.html', {'votings': votings})


def voting_detail(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    options = voting.options.annotate(vote_count=Count('votes'))
    selected_option = None
    if request.user.is_authenticated:
        selected_option = Vote.objects.filter(voting=voting, user=request.user).values_list('option_id', flat=True).first()
    return render(request, 'votings/detail.html', {
        'voting': voting,
        'options': options,
        'selected_option': selected_option,
    })


@login_required
def cast_vote(request, pk):
    if request.method != 'POST':
        return redirect('votings:detail', pk=pk)

    voting = get_object_or_404(Voting, pk=pk, is_active=True)
    option = get_object_or_404(VotingOption, pk=request.POST.get('option'), voting=voting)
    Vote.objects.update_or_create(voting=voting, user=request.user, defaults={'option': option})
    messages.success(request, 'Ваш голос збережено.')
    return redirect('votings:detail', pk=voting.pk)


@login_required
@moderator_required
def create_voting(request):
    form = VotingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        voting = form.save(commit=False)
        voting.author = request.user
        voting.save()
        VotingOption.objects.bulk_create(
            VotingOption(voting=voting, text=text) for text in form.cleaned_data['options']
        )
        messages.success(request, 'Голосування створено.')
        return redirect('votings:detail', pk=voting.pk)
    return render(request, 'votings/form.html', {'form': form})


@login_required
@moderator_required
def toggle_voting(request, pk):
    if request.method == 'POST':
        voting = get_object_or_404(Voting, pk=pk)
        voting.is_active = not voting.is_active
        voting.save(update_fields=['is_active'])
        messages.success(request, 'Статус голосування оновлено.')
    return redirect('votings:detail', pk=pk)
