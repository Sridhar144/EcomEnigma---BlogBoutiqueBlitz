from django.contrib import admin
from .models import Contact, Posts, BlogComment, Profile
# Register your models here.
admin.site.register(Contact)
admin.site.register((Posts, BlogComment))
admin.site.register(Profile)