# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from forms import PlayerFilterEmailForm, PlayerChangeForm, LogFilterForm
from models import Players, LogGameEvents, PlayerAchievements, PlayerSessions, PlayerStats
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE
from ox_game.settings import NUMBER_OF_RECORDS_AT_THE_PAGE_LOG

# Create your views here.

@login_required
def show_home_page(request):
    '''
    players = Players.objects.all()
    #
    #   Date From
    #
    date_from_post = request.POST.get('date_from')
    date_from_get = request.GET.get('date_from')
    if date_from_post:
        return HttpResponseRedirect('?date_from={}'.format(date_from_post))
    if date_from_get:
        players = Players.objects.filter(created__gte=date_from_get)
    #
    #   ID
    #
    id_post = request.POST.get('id')
    id_get = request.GET.get('id')
    if id_post:
        return HttpResponseRedirect('?id={}'.format(id_post))
    if id_get:
        players = Players.objects.filter(id=id_get)
    #
    #   Email
    #
    email_post = request.POST.get('email')
    email_get = request.GET.get('email')
    if email_post:
        return HttpResponseRedirect('?email={}'.format(email_post))
    if email_get:
        players = Players.objects.filter(email=email_get)


    context = {
        "players": players,
    }
    '''
    return render(request, 'home.html')


@login_required
def show_users(request):

    form = PlayerFilterEmailForm(request.POST or None)

    page = request.GET.get('page')
    if page == u'None' or page is None:
        page = 1
    page = int(page)
    prev_page = page - 1
    next_page = page + 1

    pages_count = Players.objects.count()
    pages_amount = pages_count / NUMBER_OF_RECORDS_AT_THE_PAGE
    if pages_count / NUMBER_OF_RECORDS_AT_THE_PAGE != pages_count / float(NUMBER_OF_RECORDS_AT_THE_PAGE):
        pages_amount += 1

    players = Players.objects.all()[NUMBER_OF_RECORDS_AT_THE_PAGE*prev_page:NUMBER_OF_RECORDS_AT_THE_PAGE*page]

    context = {
        "title": 'Users table',
        "players": players,
        "form": form,
        "page": page,
        "pages_amount": pages_amount,
        "prev_page": prev_page,
        "next_page": next_page,
        "filtered": 0,
    }

    email_post = request.POST.get('email')
    email_get = request.GET.get('email')
    if email_post:
        return HttpResponseRedirect('?email={}'.format(email_post))
    if email_get:
        players = Players.objects.filter(email=email_get)
        form = PlayerFilterEmailForm(request.POST or None)
        context = {
            "email": email_get,
            "form": form,
            "players": players,
            "page": page,
            "pages_amount": pages_amount,
            "prev_page": prev_page,
            "next_page": next_page,
            "filtered": 1,
        }
        return render(request, 'players.html', context)

    return render(request, 'players.html', context)


@permission_required('polls.can_vote')
def change_xp(request, player_id):
    # Feature #15

    player_id = request.path.split('/')[2]
    player = Players.objects.get(id=player_id)
    form = PlayerChangeForm(data={"xp": player.xp})
    template_data = {
        "form": form,
        "player": player
    }
    if request.method == 'POST':
        form = PlayerChangeForm(request.POST)
        if form.is_valid():
            player.xp = player.xp + form.cleaned_data["xp"]
            player.save()
            return HttpResponseRedirect("/users/")
    return render(request, 'players_change_xp.html', template_data)


@login_required
def show_logs(request):
    # Feature #22
    form = LogFilterForm(request.POST or None)

    page = request.GET.get('page')
    if page == u'None' or page is None:
        page = 1
    page = int(page)
    prev_page = page - 1
    next_page = page + 1

    pages_count = LogGameEvents.objects.count()
    pages_amount = pages_count / NUMBER_OF_RECORDS_AT_THE_PAGE_LOG
    if pages_count / NUMBER_OF_RECORDS_AT_THE_PAGE != pages_count / float(NUMBER_OF_RECORDS_AT_THE_PAGE_LOG):
        pages_amount += 1

    logs = LogGameEvents.objects.all()[
           NUMBER_OF_RECORDS_AT_THE_PAGE_LOG*prev_page:NUMBER_OF_RECORDS_AT_THE_PAGE_LOG*page
           ]

    player_id = request.GET.get('player_id')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    filtered = 0
    if player_id or from_date or to_date:
        filtered = 1
        logs = LogGameEvents.objects
    if player_id != u'None' and player_id is not None:
        logs = logs.filter(player_id=player_id)
    if from_date != u'None' and from_date is not None:
        logs = logs.filter(created__gte=from_date)
    if to_date != u'None' and to_date is not None:
        logs = logs.filter(created__lte=to_date)

    # paginator = Paginator(logs, NUMBER_OF_RECORDS_AT_THE_PAGE_LOG)
    # page = request.GET.get('page')
    # try:
    #     logs = paginator.page(page)
    # except PageNotAnInteger:
    #     logs = paginator.page(1)
    # except EmptyPage:
    #     logs = paginator.page(paginator.num_pages)

    context = {
        "title": 'Logs table',
        "logs": logs,
        "form": form,
        "player_id": player_id,
        "from_date": from_date,
        "to_date": to_date,
        "page": page,
        "pages_amount": pages_amount,
        "prev_page": prev_page,
        "next_page": next_page,
        "filtered": filtered,
    }

    if form.is_valid():
        from_date = form.cleaned_data.get("from_date")
        to_date = form.cleaned_data.get("to_date")
        player_id = form.cleaned_data.get("player_id")

        out_redirect_string = "?"
        if player_id:
            out_redirect_string += "player_id={}".format(player_id)
            if from_date:
                out_redirect_string += "&from_date={}".format(from_date)
            if to_date:
                out_redirect_string += "&to_date={}".format(to_date)
        elif from_date:
                out_redirect_string += "from_date={}".format(from_date)
                if to_date:
                    out_redirect_string += "&to_date={}".format(to_date)
        else:
            out_redirect_string += "to_date={}".format(to_date)
        form = LogFilterForm(request.POST or None)
        context = {
            "title": 'Filtered Logs table',
            "logs": logs,
            "form": form,
            "player_id": player_id,
            "from_date": from_date,
            "to_date": to_date,
            "page": page,
            "pages_amount": pages_amount,
            "prev_page": prev_page,
            "next_page": next_page,
            "filtered": 1,
        }
        return HttpResponseRedirect(out_redirect_string)

    return render(request, 'logs.html', context)


#
#   Authorization
#
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


# Feature #11
@login_required
def show_user_info(request):

    player_id = request.GET.get('player_id')

    player = Players.objects.get(id=player_id)

    sessions = PlayerSessions.objects.filter(player_id=player_id).order_by('-id')[:10]
    sessions = sessions.reverse()

    stats = PlayerStats.objects.filter(player_id=player_id)

    logs = LogGameEvents.objects.filter(player_id=player_id).order_by('-id')[:20]
    logs = logs.reverse()

    achievements = PlayerAchievements.objects.all()

    # LogGameEvents, PlayerAchievements, PlayerSessions, PlayerStats

    context = {
        "player": player,
        "sessions": sessions,
        "stats": stats,
        "logs": logs,
        "achievements": achievements,
        }
    return render(request, 'user.html', context)












