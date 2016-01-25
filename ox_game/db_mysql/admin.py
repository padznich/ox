from django.contrib import admin

#
# Feature #3
#
from models import Players, PlayerAchievements, PlayerSessions, PlayerStats, LogGameEvents

# Register your models here.

admin.site.register([Players, PlayerAchievements, PlayerSessions, PlayerStats, LogGameEvents])
