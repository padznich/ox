# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class LogGameEvents(models.Model):
    id = models.BigIntegerField(primary_key=True)
    player = models.ForeignKey('Players')
    event_type = models.IntegerField()
    event_data = models.TextField()
    created = models.DateTimeField()

    def __unicode__(self):
        return u"event_type={}".format(self.event_type)

    class Meta:
        managed = False
        db_table = 'log_game_events'
        verbose_name_plural = 'LogGameEvents'


class PlayerAchievements(models.Model):
    player = models.ForeignKey('Players')
    achievement_id = models.IntegerField()
    created = models.DateTimeField()

    def __unicode__(self):
        return u"achievement_id={}".format(self.achievement_id)

    class Meta:
        managed = False
        verbose_name_plural = 'PlayerAchievements'
        db_table = 'player_achievements'
        unique_together = (('player', 'achievement_id'),)


class PlayerSessions(models.Model):
    player = models.ForeignKey('Players')
    sid = models.CharField(unique=True, max_length=40)
    ip_addr = models.CharField(max_length=25, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __unicode__(self):
        return u"sid={}".format(self.sid)

    class Meta:
        managed = False
        db_table = 'player_sessions'
        verbose_name_plural = 'PlayerSesseions'


class PlayerStats(models.Model):
    id = models.IntegerField(primary_key=True)
    player = models.ForeignKey('Players')
    stat_id = models.IntegerField()
    value = models.IntegerField()

    def __unicode__(self):
        return u"stat_id={}".format(self.stat_id)

    class Meta:
        managed = False
        db_table = 'player_stats'
        verbose_name_plural = 'PlayersStats'


class Players(models.Model):
    nickname = models.CharField(unique=True, max_length=50)
    xp = models.IntegerField()
    email = models.CharField(unique=True, max_length=200)
    password_hash = models.CharField(max_length=200)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __unicode__(self):
        return u"nickname={}, email={}".format(self.nickname, self.email)

    class Meta:
        managed = False
        db_table = 'players'
        verbose_name_plural = 'Players'
