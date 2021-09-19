from django.contrib import admin

from unesco.models import Category,Iso,Site,State,Region

# Register your models here.
admin.site.register(Category)
admin.site.register(Iso)
admin.site.register(State)
admin.site.register(Site)
admin.site.register(Region)
