from django.contrib import admin
from remiljscrumy.models import GoalStatus, ScrumyGoals, ScrumyHistory,User
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(GoalStatus)
admin.site.register(ScrumyHistory)
admin.site.register(ScrumyGoals)
#admin.site.register(User)