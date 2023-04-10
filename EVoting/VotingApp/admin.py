from django.contrib import admin
# Register your models here.

from VotingApp.models import *


class admin_Election(admin.ModelAdmin):
    list_display = ['party', 'candidate_name', 'category', 'status']


class admin_Election_category(admin.ModelAdmin) :
    list_display = ['category', 'status']


admin.site.register(Election_category, admin_Election_category)
admin.site.register(Status)
admin.site.register(Election, admin_Election)

admin.site.register(aadhaarDB)
admin.site.register(registeredUsers)
