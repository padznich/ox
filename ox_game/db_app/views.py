# coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect

from forms import PlayerFilterEmailForm, PlayerChangeForm, LogFilterForm
from models import Players, LogGameEvents
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE_LOG

# Create your views here.


def show_home_page(request):
    return render(request, 'home.html')


def show_users(request):

    form = PlayerFilterEmailForm(request.POST or None)
    players = Players.objects.all()

    # Feature #6
    paginator = Paginator(players, NUMBER_OF_RECORDS_AT_THE_PAGE)
    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)

    context = {
        "title": 'Users table',
        "players": players,
        "form": form
    }

    if form.is_valid():
        # Feature #7
        email = form.cleaned_data.get("email")
        form.email = request.POST["email"]          #######
        form = PlayerFilterEmailForm(request.POST or None)
        players = Players.objects.filter(email=email)
        paginator = Paginator(players, NUMBER_OF_RECORDS_AT_THE_PAGE)
        page = request.GET.get('page')
        try:
            players = paginator.page(page)
        except PageNotAnInteger:
            players = paginator.page(1)
        except EmptyPage:
            players = paginator.page(paginator.num_pages)
        context = {
            "title": 'Filtered Users table',
            "players": players,
            "email": email,
            "form": form,
        }

        return render(request, 'players.html', context)

    return render(request, 'players.html', context)


def change_xp(request, player_id):
    # Feature #15
    player = Players.objects.get(id=player_id)
    form = PlayerChangeForm(data={"xp": player.xp})
    template_data = {
        "form": form,
        "player": player
    }

    if request.method == 'POST':
        form = PlayerChangeForm(request.POST)
        if form.is_valid():
            player.xp = form.cleaned_data["xp"]
            player.save()
            return HttpResponseRedirect("/users/")

    return render(request, 'players_change_xp.html', template_data)


def show_logs(request):
    # Feature #22
    form = LogFilterForm(request.POST or None)

    logs = LogGameEvents.objects.all()

    paginator = Paginator(logs, NUMBER_OF_RECORDS_AT_THE_PAGE)
    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)

    context = {
        "title": 'Logs table',
        "logs": logs,
        "form": form
    }

    if form.is_valid():

        from_date = form.cleaned_data.get("from_date")
        to_date = form.cleaned_data.get("to_date")
        player_id = form.cleaned_data.get("player_id")

        form = LogFilterForm(request.POST or None)

        logs = LogGameEvents.objects.all()
        if player_id:
            logs = logs.filter(player_id=player_id)
        if from_date:
            logs = logs.filter(created__gte=from_date)
        if to_date:
            logs = logs.filter(created__lte=to_date)

        paginator = Paginator(logs, NUMBER_OF_RECORDS_AT_THE_PAGE_LOG)
        page = request.GET.get('page')
        try:
            logs = paginator.page(page)
        except PageNotAnInteger:
            logs = paginator.page(1)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)
        context = {
            "title": 'Filered Logs table',
            "logs": logs,
            "from_date": from_date,
            "to_date": to_date,
            "player_id": player_id,
            "form": form,
        }
        return render(request, 'logs_filtered.html', context)
    return render(request, 'logs.html', context)


#
#   Authorization
#
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class ListContactView(LoggedInMixin):

    model = Players
    template_name = 'players.html'

    # LOGIN_URL = 'django.contrib.auth.views.login'

    def get_queryset(self):

        return Players.objects.filter(owner=self.request.user)















