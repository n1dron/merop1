from django.contrib import admin
from django.db.models import Count, Sum
from .models import SportType, Event, Team, ParticipationRequest

@admin.register(SportType)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'participant_count', 'team_count')
    list_filter = ('sport_type', 'date')
    search_fields = ('title', 'location')
    date_hierarchy = 'date'
    
    def participant_count(self, obj):
        # Более точный подсчет уникальных участников через агрегацию
        return obj.teams.aggregate(
            total=Count('members', distinct=True)
        )['total']
    participant_count.short_description = 'Участников'
    
    def team_count(self, obj):
        return obj.teams.count()
    team_count.short_description = 'Команд'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport_type', 'captain', 'member_count')
    list_filter = ('sport_type',)
    search_fields = ('name', 'captain__username')
    raw_id_fields = ('captain',)
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Участников'

@admin.register(ParticipationRequest)
class ParticipationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'status', 'created_at')
    list_filter = ('status', 'team__sport_type')
    search_fields = ('user__username', 'team__name')
    date_hierarchy = 'created_at'
    list_editable = ('status',)
    actions = ['approve_requests']
    
    def approve_requests(self, request, queryset):
        queryset.update(status='approved')
    approve_requests.short_description = 'Одобрить выбранные заявки'