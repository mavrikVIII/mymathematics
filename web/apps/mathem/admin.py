from django.contrib import admin

from .models import Question, Comment, PeoplesErrors, Profile

admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(PeoplesErrors)
admin.site.register(Profile)
