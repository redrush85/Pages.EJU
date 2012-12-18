__author__ = 'RedRush'
from django.contrib import admin
from Catalog.models import category, url

class categoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    ordering = ('id',)

class urlAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'description', 'category', 'date')
    list_filter = ('category', 'date')
    ordering = ('-id',)
    list_per_page = 20
    search_fields = ['title']
    date_hierarchy = 'date'

admin.site.register(category, categoryAdmin)
admin.site.register(url, urlAdmin)



