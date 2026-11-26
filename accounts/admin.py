from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile Details"
    fields = ("phone", "city")


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ("username", "email", "first_name", "last_name", "get_phone", "get_city", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "profile__phone", "profile__city")

    def get_phone(self, obj):
        return getattr(obj, "profile", None) and obj.profile.phone
    get_phone.short_description = "Phone"

    def get_city(self, obj):
        return getattr(obj, "profile", None) and obj.profile.city
    get_city.short_description = "City"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "city")
    search_fields = ("user__username", "user__email", "phone", "city")
