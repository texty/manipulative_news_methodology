from django.contrib import admin
from . import models

class ArticleAdmin(admin.ModelAdmin):
    list_filter = ['bee']
    search_fields = ['real_url', 'ra_title']

class ClassifiedAdmin(admin.ModelAdmin):
    list_filter = ['article__bee', 'types']
    search_fields = ['article__real_url', 'article__ra_title']

class Ner_entityAdmin(admin.ModelAdmin):
    list_filter = ['entity_type', 'article__bee']
    search_fields = ['article__real_url', 'article__ra_title']

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Classified, ClassifiedAdmin)
admin.site.register(models.FakeType)
admin.site.register(models.Feedback)