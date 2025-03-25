from django.contrib import admin

from member.forms import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...