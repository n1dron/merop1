from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView, DetailView, CreateView, 
    UpdateView, DeleteView, TemplateView, View
)
from django.urls import reverse, reverse_lazy
from django.utils import timezone
import json
from django.core.serializers import serialize
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.http import require_GET

from .forms import EventFilterForm, EventForm
from .models import Event, Team, ParticipationRequest
from .mixins import TeacherRequiredMixin


@require_GET
def event_list(request):
    events = Event.objects.all().order_by('-date')  # Сортировка по дате
    form = EventFilterForm(request.GET or None)
    
    if form.is_valid():
        if form.cleaned_data['sport_type']:
            events = events.filter(sport_type=form.cleaned_data['sport_type'])
        if form.cleaned_data['date_from']:
            events = events.filter(date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data['date_to']:
            events = events.filter(date__lte=form.cleaned_data['date_to'])

    return render(request, 'events/event_list.html', {
        'events': events,
        'form': form
    })

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


def team_list(request):
    teams = Team.objects.all().select_related('sport_type', 'captain').prefetch_related('members')
    
    return render(request, 'events/team_list.html', {
        'teams': teams,
        'title': 'Список команд'
    })

def home(request):
    return render(request, 'events/home.html')


@login_required
def create_participation_request(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    
    if ParticipationRequest.objects.filter(user=request.user, team=team).exists():
        messages.warning(request, 'Вы уже подавали заявку в эту команду')
    else:
        ParticipationRequest.objects.create(
            user=request.user,
            team=team,
            status='pending'
        )
        messages.success(request, 'Заявка успешно подана')
    
    return redirect('team_list')


class ParticipationRequestList(TeacherRequiredMixin, ListView):
    model = ParticipationRequest
    template_name = 'events/request_list.html'
    context_object_name = 'requests'
    
    def get_queryset(self):
        return ParticipationRequest.objects.filter(status='pending').select_related('user', 'team')


class ProcessRequestView(TeacherRequiredMixin, UpdateView):
    model = ParticipationRequest
    fields = ['status']
    template_name = 'events/process_request.html'
    success_url = reverse_lazy('request_list')
    
    def form_valid(self, form):
        if form.cleaned_data['status'] == 'approved':
            self.object.team.members.add(self.object.user)
        messages.success(self.request, 'Заявка успешно обработана')
        return super().form_valid(form)


class TeamCreateView(TeacherRequiredMixin, CreateView):
    model = Team
    fields = ['name', 'sport_type', 'captain', 'required_players']
    template_name = 'events/team_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Команда успешно создана')
        return reverse('team_list')


class TeamUpdateView(TeacherRequiredMixin, UpdateView):
    model = Team
    fields = ['name', 'sport_type', 'captain', 'required_players']
    template_name = 'events/team_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Команда успешно обновлена')
        return reverse('team_list')


class TeamDeleteView(TeacherRequiredMixin, DeleteView):
    model = Team
    template_name = 'events/team_confirm_delete.html'
    success_url = reverse_lazy('team_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Подтверждение удаления команды"
        context['member_count'] = self.object.members.count()
        return context
    
    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        messages.success(request, f'Команда "{team.name}" успешно удалена')
        return super().delete(request, *args, **kwargs)


class EventCreateView(TeacherRequiredMixin, CreateView):
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Создание мероприятия"
        return context
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Мероприятие успешно создано!")
        return response
    
    def get_success_url(self):
        return reverse('event_detail', kwargs={'pk': self.object.pk})

class EventUpdateView(TeacherRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование мероприятия"
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Мероприятие успешно обновлено!")
        return response
    
    def get_success_url(self):
        return reverse('event_list')

class EventDeleteView(TeacherRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Мероприятие успешно удалено!")
        return response


class TeamDetailView(DetailView):
    model = Team
    template_name = 'events/team_detail.html'
    context_object_name = 'team'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object
        members = team.members.all()
        
        context.update({
            'captain': team.captain,
            'regular_members': members.exclude(id=team.captain.id),
            'spots_left': max(0, team.required_players - members.count())
        })
        return context


@method_decorator(login_required, name='dispatch')
class TeacherDashboardView(TemplateView):
    template_name = 'teacher/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Получаем команды без annotate, так как используем свойство модели
        active_teams = Team.objects.all().order_by('-created_at')[:5]
        
        context.update({
            'active_events': Event.objects.filter(date__gte=today).order_by('date')[:5],
            'active_teams': active_teams,
            'pending_requests': ParticipationRequest.objects.filter(
                status='pending'
            ).select_related('user', 'team')[:5],
            'stats': {
                'total_teams': Team.objects.count(),
                'active_events_count': Event.objects.filter(date__gte=today).count(),
                'pending_requests_count': ParticipationRequest.objects.filter(
                    status='pending'
                ).count(),
            }
        })
        return context


class BulkApproveView(TeacherRequiredMixin, View):
    def post(self, request):
        selected = request.POST.getlist('selected_requests')
        
        if not selected:
            messages.warning(request, 'Не выбрано ни одной заявки')
            return redirect('request_list')

        ParticipationRequest.objects.filter(id__in=selected).update(status='approved')
        messages.success(request, f'{len(selected)} заявок одобрено')
        return redirect('request_list')