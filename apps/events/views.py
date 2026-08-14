import calendar as pycalendar
from datetime import date, datetime, time, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Coalesce
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from apps.accounts.mixins import ModeratorOrAdminRequiredMixin

from .forms import EventForm
from .models import Event

MONTH_NAMES = (
    'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
    'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень',
)
WEEKDAY_NAMES = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд')


def events_between(start_date, end_date):
    """Події, що перетинаються з проміжком дат (включно), разом із багатоденними."""
    tz = timezone.get_current_timezone()
    range_start = timezone.make_aware(datetime.combine(start_date, time.min), tz)
    range_end = timezone.make_aware(datetime.combine(end_date, time.max), tz)
    return (
        Event.objects
        .annotate(effective_end=Coalesce('ends_at', 'starts_at'))
        .filter(starts_at__lte=range_end, effective_end__gte=range_start)
        .select_related('author')
    )


class EventListView(generic.ListView):
    """Список подій: майбутні (за замовчуванням), минулі або всі."""
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.select_related('author')
        now = timezone.now()
        if self.request.GET.get('filter') == 'past':
            return queryset.annotate(effective_end=Coalesce('ends_at', 'starts_at')) \
                           .filter(effective_end__lt=now).order_by('-starts_at')
        if self.request.GET.get('filter') == 'all':
            return queryset
        return queryset.annotate(effective_end=Coalesce('ends_at', 'starts_at')) \
                       .filter(effective_end__gte=now)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'upcoming')
        return context


class EventCalendarView(generic.TemplateView):
    """Календар подій на місяць: сітка тижнів із подіями в клітинках."""
    template_name = 'events/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        year = self.kwargs.get('year', today.year)
        month = self.kwargs.get('month', today.month)
        if not 1 <= month <= 12 or not 1 <= year <= 9999:
            raise Http404('Такого місяця не існує.')

        month_start = date(year, month, 1)
        weeks_dates = pycalendar.Calendar(firstweekday=0).monthdatescalendar(year, month)
        events_by_day = self._group_by_day(weeks_dates[0][0], weeks_dates[-1][-1])

        context['weeks'] = [
            [{
                'date': day,
                'in_month': day.month == month,
                'is_today': day == today,
                'events': events_by_day.get(day, []),
            } for day in week]
            for week in weeks_dates
        ]
        context['weekday_names'] = WEEKDAY_NAMES
        context['month_title'] = f'{MONTH_NAMES[month - 1]} {year}'
        context['today'] = today
        context['prev_month'] = month_start - timedelta(days=1)
        context['next_month'] = (month_start + timedelta(days=32)).replace(day=1)
        return context

    @staticmethod
    def _group_by_day(first_day, last_day):
        """Розкладає події по днях; багатоденна подія потрапляє в кожен свій день."""
        events_by_day = {}
        for event in events_between(first_day, last_day):
            day = max(event.start_date, first_day)
            final_day = min(event.end_date, last_day)
            while day <= final_day:
                events_by_day.setdefault(day, []).append(event)
                day += timedelta(days=1)
        return events_by_day


class EventDayView(generic.TemplateView):
    """Події конкретного дня — відкривається кліком по клітинці календаря."""
    template_name = 'events/day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            day = date(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'])
        except ValueError:
            raise Http404('Такої дати не існує.')
        context['day'] = day
        context['events'] = events_between(day, day)
        context['month_title'] = f'{MONTH_NAMES[day.month - 1]} {day.year}'
        return context


class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'events/detail.html'


class EventCreateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Подію створено.')
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    context_object_name = 'event'

    def form_valid(self, form):
        messages.success(self.request, 'Подію оновлено.')
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, ModeratorOrAdminRequiredMixin, generic.DeleteView):
    model = Event
    template_name = 'events/confirm_delete.html'
    context_object_name = 'event'
    success_url = reverse_lazy('events:list')

    def form_valid(self, form):
        messages.success(self.request, 'Подію видалено.')
        return super().form_valid(form)
