from django.contrib import admin
from .models import Article, Tag, ArticleTag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=['title','author','status','created_at','published_at']
    list_filter=['status','published_at','created_at']
    search_fields=['title','content']
    prepopulated_fields={'slug':('title' ,)}
    date_hierarchy='created_at'
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['name', 'slug']
    search_fields=['name']
    prepopulated_fields={'slug':('name',)}
    
@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display=['article','tag']
    list_filter=['tag']