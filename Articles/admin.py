from django.contrib import admin
from Articles.models import Article,ArticleTest
# Register your models here.

class ArticleAdmnin(admin.ModelAdmin):
    pass
admin.site.register(Article,ArticleAdmnin)
admin.site.register(ArticleTest)