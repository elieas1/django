from django.contrib import admin

from .models import Resume, Job, GeneralResume
# Register your models here.


class UnitInline(admin.TabularInline):
    model = Resume
    extra = 1


class JobAdmin(admin.ModelAdmin):
    inlines = [
        UnitInline,
    ]

    list_display = ('title', 'active', 'date','location')

    def delete_queryset(self, request, query):
        for q in query:
            q.delete()


admin.site.register(Job, JobAdmin)


class ResumeAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, query):
        for q in query:
            q.delete()


admin.site.register(Resume, ResumeAdmin)


class GeneralResumeAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, query):
        for q in query:
            q.delete()


admin.site.register(GeneralResume, GeneralResumeAdmin)
