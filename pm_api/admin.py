from django.contrib import admin

from pm_api import models


# Register your models here.
# enable newly created models to display in admin interface
admin.site.register(models.UserProfile)