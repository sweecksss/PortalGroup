from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

from .models import ForumCategory
from .forms import ForumCategoryForm, ForumMessageForm


class ModeratorRequiredMixin(UserPassesTestMixin):
    """Доступ тільки для модераторів/адмінів (створення й видалення веток)."""

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.role in ['moderator', 'admin'] or user.is_superuser)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.info(self.request, 'Щоб продовжити, увійдіть у акаунт.')
            return redirect('accounts:login')
        messages.error(self.request, 'У вас немає прав для цієї дії.')
        return redirect('forum:category_list')


class CategoryListView(generic.ListView):
    """Список усіх веток форуму."""
    model = ForumCategory
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(generic.detail.SingleObjectMixin, generic.FormView):
    """Перегляд повідомлень ветки + форма додавання нового повідомлення."""
    template_name = 'forum/category_detail.html'
    form_class = ForumMessageForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=ForumCategory.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=ForumCategory.objects.all())
        if not request.user.is_authenticated:
            messages.info(request, 'Щоб писати повідомлення, потрібно увійти в акаунт.')
            return redirect('accounts:login')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        context['messages_list'] = self.object.messages.select_related('author')
        return context

    def form_valid(self, form):
        message = form.save(commit=False)
        message.category = self.object
        message.author = self.request.user
        message.save()
        messages.success(self.request, 'Повідомлення додано.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('forum:category_detail', kwargs={'pk': self.object.pk})


class CategoryCreateView(LoginRequiredMixin, ModeratorRequiredMixin, generic.CreateView):
    """Створення нової ветки (тільки модератор/адмін)."""
    model = ForumCategory
    form_class = ForumCategoryForm
    template_name = 'forum/category_form.html'
    success_url = reverse_lazy('forum:category_list')
    login_url = 'accounts:login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Тему "{form.instance.name}" створено.')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, ModeratorRequiredMixin, generic.UpdateView):
    """Редагування ветки (тільки модератор/адмін)."""
    model = ForumCategory
    form_class = ForumCategoryForm
    template_name = 'forum/category_form.html'
    login_url = 'accounts:login'

    def get_success_url(self):
        messages.success(self.request, f'Тему "{self.object.name}" оновлено.')
        return reverse('forum:category_detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, ModeratorRequiredMixin, generic.DeleteView):
    """Видалення ветки (тільки модератор/адмін)."""
    model = ForumCategory
    template_name = 'forum/category_confirm_delete.html'
    success_url = reverse_lazy('forum:category_list')
    login_url = 'accounts:login'

    def form_valid(self, form):
        messages.success(self.request, f'Тему "{self.object.name}" видалено.')
        return super().form_valid(form)
