from django.contrib import admin
from .models import PersonDetails, Person, Blogs, Blog

# Register your models here.
class PersonDetailsAdmin(admin.ModelAdmin):
    list_display = ['gender', 'age', 'dob', ]

class PersonAdmin(admin.ModelAdmin):
    list_display =['person', '_age', '_gender']

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title']

class BlogsAdmin(admin.ModelAdmin):
    list_display = ['_person_name', '_blog_title', '_date_created']

admin.site.register(PersonDetails, PersonDetailsAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Blog, BlogAdmin)