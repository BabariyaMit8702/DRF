from django.contrib import admin
from .models import collage,student,company,employee

class companyadm(admin.ModelAdmin):
    list_display = ('name','location')
    search_fields = ['name']

class empadm(admin.ModelAdmin):
    list_filter = ['company']

# Register your models here.
admin.site.register(collage)
admin.site.register(student)
admin.site.register(company,companyadm)
admin.site.register(employee,empadm)