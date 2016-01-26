from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

from models import Players
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE


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


def home(request):
    template_data = {
        "player_list": Players.objects.all()
    }

    return render(request, 'base.html', template_data)
