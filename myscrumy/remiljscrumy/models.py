from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class GoalStatus(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.status_name
    class Meta:
        verbose_name_plural = "Goal Status"
    
class ScrumyGoals(models.Model):
    goal_name= models.CharField(max_length=200)
    goal_id= models.CharField(max_length=200)
    created_by = models.CharField(max_length=200)
    moved_by = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')

    def __str__(self):
        return self.goal_name

    class Meta:
        verbose_name_plural = "Scrumy Goals"


class ScrumyHistory(models.Model):
    moved_by = models.CharField(max_length=200)
    created_by = models.CharField(max_length=200)
    moved_from = models.CharField(max_length=200)
    moved_to = models.CharField(max_length=200)
    time_of_action = models.DateTimeField(auto_now=False, auto_now_add=False)
    goal=models.ForeignKey(ScrumyGoals, on_delete=models.CASCADE)

    
    def __str__(self):
         return self.created_by
    class Meta:
        verbose_name_plural = "Scrumy History"
