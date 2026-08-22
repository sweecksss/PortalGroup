from django.contrib.auth import get_user_model
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import generic

from apps.announcements.models import Announcement
from apps.events.models import Event
from apps.forum.models import ForumCategory, ForumMessage
from apps.gallery.models import Photo
from apps.materials.models import Material
from apps.surveys.models import Survey
from apps.votings.models import Voting


class HomeView(generic.TemplateView):
    """Головна сторінка: коротка інформація про групу та віджети розділів порталу."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

        context['upcoming_events'] = (
            Event.objects
            .annotate(effective_end=Coalesce('ends_at', 'starts_at'))
            .filter(effective_end__gte=now)
            .order_by('starts_at')[:4]
        )
        context['announcements'] = Announcement.objects.select_related('author')[:4]
        context['forum_messages'] = (
            ForumMessage.objects.select_related('author', 'category').order_by('-created_at')[:4]
        )
        context['surveys'] = Survey.objects.filter(is_active=True).order_by('-created_at')[:3]
        context['votings'] = Voting.objects.filter(is_active=True)[:3]
        context['materials'] = Material.objects.select_related('author')[:4]
        context['photos'] = Photo.objects.select_related('album')[:6]

        context['stats'] = {
            'users': get_user_model().objects.count(),
            'events': Event.objects.count(),
            'forum_categories': ForumCategory.objects.count(),
            'materials': Material.objects.count(),
        }
        return context


def toggle_theme(request):
    """Перемикає світлу й темну тему та повертає користувача на ту саму сторінку."""
    request.session['theme'] = 'light' if request.session.get('theme') == 'dark' else 'dark'

    next_url = request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()},
                                                    require_https=request.is_secure()):
        return redirect(next_url)
    return redirect('home')
