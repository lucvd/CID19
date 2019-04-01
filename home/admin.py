from django.contrib import admin

from .models import Profile, Project, SuccessStory


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'linkedin', 'headline', 'profilePicture', 'bio', 'get_favorites', 'whyImHere']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created', 'visible', 'anonymity']

class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'website']

admin.site.register(Project, ProjectAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(SuccessStory, SuccessStoryAdmin)