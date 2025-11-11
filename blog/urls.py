from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, TagViewSet

router=DefaultRouter()
"""
basename='abc' 
allows Django name your URL patterns: abc-list, abc-detail, abc-.. etc ....
"""
router.register(r'article', ArticleViewSet, basename='article')
router.register(r'tag', TagViewSet, basename='tag')

urlpatterns=[
    path('', include(router.urls)),
]