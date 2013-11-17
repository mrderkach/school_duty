from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    position = models.CharField(max_length=200)
    human_amount = models.IntegerField(default=2)
    
    def __str__(self):
        return self.position
    
    def free(self):
        return self.human_amount - self.userchoice_set.count()

class UserChoice(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    date = models.DateTimeField('date booked')
    
    def __str__(self):
        return str(self.user)