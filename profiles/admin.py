from django.contrib import admin

from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
	model = Profile
	list_display = ('name', 'description',)
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Profile, ProfileAdmin)
