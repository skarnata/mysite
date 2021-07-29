from django.contrib import admin
from .models import Post, Category, Comment
from mptt.admin import MPTTModelAdmin


# Register your models here.
@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug', 'author')
    prepopulated_fields = {
        'slug': ('title',),
    }


admin.site.register(Comment, MPTTModelAdmin)

admin.site.register(Category)

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('comment2post', 'name', 'email', 'publish', 'status')
#     list_filter = ('status', 'publish')
#     search_fields = ('name', 'email', 'content')
#
