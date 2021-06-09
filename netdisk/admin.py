from django.contrib import admin

from .models import File, Folder, Link

# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
admin.site.register(Link)
