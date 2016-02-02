import hashlib
import datetime
import random

from django.core.management.base import BaseCommand
from db_app.models import Players, PlayerSessions, LogGameEvents

class Command(BaseCommand):
    help = 'Fill up db with data'

    def add_arguments(self, parser):
        parser.add_argument('--player-count', default=10, type=int)
        parser.add_argument('--session-count-per-user', default=3, type=int)
        parser.add_argument('--log-count-per-user', default=3, type=int)

    def _create_log(self, player_object, log_index):
        log = LogGameEvents()
        log.id = log_index
        log.player = player_object
        log.event_type = 000
        log.event_data = 'spam'
        log.is_finished = bool(random.randint(0, 1))
        log.created = datetime.datetime.now()
        log.save()

    def _create_player(self, player_index, options):
        player = Players()
        nickname_unique_part = str(player_index) + str(datetime.datetime.now())
        nickname_unique_hash = hashlib.sha1(nickname_unique_part).hexdigest()[:10]
        player.nickname = "test_{}".format(nickname_unique_hash)
        player.email = "{}@tut.by".format(player.nickname)
        player.xp = 0
        player.created = datetime.datetime.now()
        player.updated = datetime.datetime.now()
        player.save()

        for log_index in xrange(options["log_count_per_user"]):
            self._create_log(player, log_index)

    def handle(self, *args, **options):
        for i in xrange(options["player_count"]):
            self._create_player(i, options)


if __name__ == '__main__':
    c = Command()
    c.handle({"player_count": 5})