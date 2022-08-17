from django.contrib import admin
from .models import User, Levels
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'score', 'games_played')


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', "level_id", "level_score")

