from django.contrib import admin

from .models import Blog, Image

# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, query):
        for q in query:
            q.delete()


admin.site.register(Image, ImageAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'homepage')
    list_filter = ['date']
    search_fields = ['title']

    def delete_queryset(self, request, query):
        for q in query:
            q.delete()


admin.site.register(Blog, BlogAdmin)
