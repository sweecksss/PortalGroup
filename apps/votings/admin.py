from django.contrib import admin

from .models import Vote, Voting, VotingOption


class VotingOptionInline(admin.TabularInline):
    model = VotingOption
    extra = 2


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'author', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [VotingOptionInline]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voting', 'option', 'user', 'created_at')
    list_filter = ('voting',)
