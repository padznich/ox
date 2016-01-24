from django.contrib import admin

from models import Players, PlayerAchievements, PlayerSessions, PlayerStats, LogGameEvents

# Register your models here.

admin.site.register([Players, PlayerAchievements, PlayerSessions, PlayerStats, LogGameEvents])
