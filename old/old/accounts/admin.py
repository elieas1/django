from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'username','date_joined','last_login')
    list_filter = ['last_login']
    search_fields = ['email']


admin.site.register(User, UserAdmin)
