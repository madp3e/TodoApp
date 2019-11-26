from django.contrib import admin
from .models import List, Profile


# Register your models here.

class ListAdmin(admin.ModelAdmin):
    list_display = ["content", "created_date", "completed", "author"]


admin.site.register(List, ListAdmin)
admin.site.register(Profile)
