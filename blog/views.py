from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.utils.text import slugify

from .models import Article, Tag
from .serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    TagSerializer)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit or delete their own articles.
    """

    def has_object_permission(self, request, view, obj):
        # 'Read' permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # 'Write' permissions only for the author
        return obj.author == request.user


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing articles.
    Provides search, filter, order, slug-based lookup, and publish actions.
    """

    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug' #replace numeric IDs in URLs with a readable string

    # Filtering and searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'tags']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'published_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Public users see only published articles.
        Authenticated users see all (their own drafts + published).
        """
        user = self.request.user
        queryset = Article.objects.all()

        if not user.is_authenticated:
            queryset = queryset.filter(status='published')

        # Optional tag filtering (like ?tags=python,ai)
        tags = self.request.query_params.get('tags')
        if tags:
            tag_list = [t.strip() for t in tags.split(',')]
            queryset = queryset.filter(tags__name__in=tag_list).distinct()

        return queryset

    def get_serializer_class(self):
        # lightweight serializer for list view
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer

    def perform_create(self, serializer):
        """
        Automatically set author and generate a unique slug.
        """
        title = serializer.validated_data['title']
        slug = slugify(title)
        base_slug = slug
        count = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        serializer.save(author=self.request.user, slug=slug)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, slug=None):
        """
        Publish an article (only author can do this).
        """
        article = self.get_object()
        if article.author != request.user:
            return Response(
                {"detail": "You do not have permission to publish this article."},
                status=status.HTTP_403_FORBIDDEN,
            )

        article.status = 'published'
        article.published_at = timezone.now()
        article.save()
        return Response(self.get_serializer(article).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unpublish(self, request, slug=None):
        """
        Unpublish an article (revert to draft).
        """
        article = self.get_object()
        if article.author != request.user:
            return Response(
                {"detail": "You do not have permission to unpublish this article."},
                status=status.HTTP_403_FORBIDDEN,
            )

        article.status = 'draft'
        article.published_at = None
        article.save()
        return Response(self.get_serializer(article).data)

    @action(detail=False, methods=['get'])
    def published(self, request):
        """
        List all published articles.
        """
        articles = self.get_queryset().filter(status='published')
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
