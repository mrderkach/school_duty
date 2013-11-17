from django.contrib import admin
from posts.models import UserChoice, Post
    
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Post description',      {'fields': ['position', 'human_amount']}),
    ]
    list_display = ('position', 'human_amount', 'free')
    list_filter = ['position']
    
class UserChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                    {'fields': ['user']}),
        ('Choice description',    {'fields': ['post', 'date']}),
    ]
    list_display = ('user', 'post')
    list_filter = ['user', 'post']

admin.site.register(Post, PostAdmin)
admin.site.register(UserChoice, UserChoiceAdmin)