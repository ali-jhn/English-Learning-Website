from django.contrib import admin
from .models import Lesson, Exercise, Search, Person

admin.site.register(Lesson)
admin.site.register(Person)
admin.site.register(Exercise)
admin.site.register(Search)
