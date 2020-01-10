from django.contrib import admin
from Articles.models import Article
# Register your models here.

class ArticleAdmnin(admin.ModelAdmin):
    pass
admin.site.register(Article,ArticleAdmnin)