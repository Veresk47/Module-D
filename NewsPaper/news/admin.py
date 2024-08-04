from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'categoryType', 'dateCreation', 'rating', 'title']
    list_filter = ['author', 'categoryType', 'dateCreation', 'rating']



class CommentPost(admin.ModelAdmin):
    list_display = ['commentPost', 'commentUser', 'text', 'dateCreation', 'rating',]
    list_filter = ['commentPost', 'commentUser', 'dateCreation', 'rating']
    search_fields = ['commentUser']



admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment, CommentPost)
admin.site.register(PostCategory)
# Register your models here.
