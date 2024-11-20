from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(FlashCard)
admin.site.register(FlashcardSet)
admin.site.register(FlashcardCollection)
admin.site.register(Comment)