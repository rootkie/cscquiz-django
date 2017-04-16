from django.contrib import admin

# Register your models here.
from .models import Question, Score, ActiveSet

admin.site.register(Question)
admin.site.register(Score)
admin.site.register(ActiveSet)
