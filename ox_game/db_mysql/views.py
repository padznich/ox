from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.

from models import Players, LogGameEvents

from forms import PlayerChangeForm, LogDateFilterForm, LogPlayerIdFilterForm
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE_LOG


def home(request):
    template_data = {
        "player_list": Players.objects.all()
    }
    return render(request, 'base.html', template_data)

def players_paginator(request, players_list):
    paginator = Paginator(players_list, NUMBER_OF_RECORDS_AT_THE_PAGE)
    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        players = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        players = paginator.page(paginator.num_pages)
    return render_to_response('players_list.html', {"players": players})

def players_listing(request):
    # Feature #6
    players_list = Players.objects.all()
    return players_paginator(request, players_list)

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
            return HttpResponseRedirect("/list/")

    return render(request, 'player_change_form.html', template_data)

'''
class Log: # something wrong!

    def __init__(self):
        self.log_list = LogGameEvents.objects.all()
        self.paginator = Paginator(self.log_list, NUMBER_OF_RECORDS_AT_THE_PAGE_LOG)

    def filter_player_id(self, player_id):
        self.log_list.filter(player_id=player_id)

    def list(self, request):
        self.page = request.GET.get('page')
        try:
            self.logs = self.paginator.page(self.page)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page.
            self.logs = self.paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            self.logs = self.paginator.page(self.paginator.num_pages)
        return render_to_response('log_list.html', {"logs": self.logs})
'''

def log_paginator(request, log_list):
    # Feature #22
    paginator = Paginator(log_list, NUMBER_OF_RECORDS_AT_THE_PAGE_LOG)
    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator.page(paginator.num_pages)

    return render_to_response('log_list.html', {"logs": logs})

def log_game_events_listing(request):
    # Feature #22
    log_list = LogGameEvents.objects.all()
    return log_paginator(request, log_list)

def log_date_filter(request):

    form = LogDateFilterForm(request.POST or None)
    if form.is_valid():
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        log_list = LogGameEvents.objects.filter(created__gte=from_date).filter(created__lte=to_date)
        return log_paginator(request, log_list)
    template_data = {
        "form": form,
    }
    return render(request, 'log_filter_form.html', template_data)

def log_player_id_filter(request):

    form = LogPlayerIdFilterForm(request.POST or None)
    if form.is_valid():
        player_id = form.cleaned_data.get('player_id')
        log_list = LogGameEvents.objects.filter(player_id=player_id)
        return log_paginator(request, log_list)

    template_data = {
        "form": form,
    }
    return render(request, 'log_filter_form.html', template_data)

def log_filter_by_id(request, player_id):
    # Feature #22
    log_list = LogGameEvents.objects.all().filter(player_id=player_id)
    return log_paginator(request, log_list)

def log_cool(request):

    log_list = LogGameEvents.objects.all()
    paginator = Paginator(log_list, NUMBER_OF_RECORDS_AT_THE_PAGE_LOG)
    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator.page(paginator.num_pages)

    return render_to_response('log_input.html', {"logs": logs})
