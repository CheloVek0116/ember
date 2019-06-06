from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Post)
class PostOptions(admin.ModelAdmin):
    fields = ('user', 'content')
    list_display = ('user', 'content',)
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
    )
    view_on_site = True


@admin.register(User)
class AdminOptions(admin.ModelAdmin):
    fields = ('avatar', 'first_name', 'last_name', 'username', 'password', 'sex', 'language', 'age', 'country',)
    list_display = ('username',)
    

@admin.register(Chat, Message)
class PostOptions(admin.ModelAdmin):
    pass