from django.contrib import admin
from .models import User
from .models import *

admin.site.register(Page)
admin.site.register(Chapter)
admin.site.register(Manga)
admin.site.register(Tag)
admin.site.register(NewsItem)
admin.site.register(User)
admin.site.register(ContentType)
admin.site.register(TranslatingStatus)