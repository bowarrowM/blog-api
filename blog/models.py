from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Models are the structure of your database tables
# so basically, whatever you write here will be translated into database tables.
# If there's a logic mismatch between what you desire and your instructions, your app will not work properly.

# For example, if you want to create a blog application, you might have an Article model like this:

class Article(models.Model):
    title = models.CharField(max_length=225) 
    slug = models.SlugField(max_length=225, unique=True)
    #A slug is a URL-friendly version of a title or name.It’s used to make clean, readable, SEO-friendly URLs.
    #assume your article title is "first blog!". instead of getting an url like /artciles/1 etc you will get /articles/first-blog/"
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='articles')
    body= models.TextField()
    tags = models.CharField(max_length=100, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at= models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super().save(*args, **kwargs)
        
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='article_tags')
    
    class Meta:
        unique_together = ('article', 'tag')
    #unq_2gether: prevents the same tag from being added twice to the same article.
        
    def __str__(self):
        return f"{self.article.title} - {self.tag.name}"