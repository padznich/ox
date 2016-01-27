from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.

from models import Players, LogGameEvents

from forms import PlayerChangeForm
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE_LOG


def home(request):
    template_data = {
        "player_list": Players.objects.all()
    }
    return render(request, 'base.html', template_data)

def players_listing(request):
    # Feature #6
    players_list = Players.objects.all()
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

def log_game_events_listing(request):
    # Feature #22
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

    return render_to_response('log_list.html', {"logs": logs})

def log_filter_by_id(request, player_id):
    # Feature #22
    # log_list = LogGameEvents.objects.all().order_by('player_id')
    log_list = LogGameEvents.objects.all().filter(player_id=player_id)
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

def log_filter_by_date_created(request, from_date, to_date):
    # Feature #22
    log_list = LogGameEvents.objects.filter(created__gte=from_date).filter(created__lte=to_date)
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


def change_xp(request, player_id):
    # Feature #15
    player = Players.objects.get(id=player_id)
    form = PlayerChangeForm(data={"nickname": player.nickname, "email": player.email, "xp": player.xp})
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

    return render(request, 'change_player_form.html', template_data)


