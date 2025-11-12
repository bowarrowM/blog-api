from rest_framework import serializers
from .models import Article, Tag, ArticleTag

""" 
Metaprogramming is the practice of writing code that manipulates or generates other code.
example:
a class: defines the behaviors of objects within,
a metaclass: defines the behaviours of classes themselves and the instances as well
"""

class TagSerializer(serializers.ModelSerializer): #Converts Tag model to/from JSON
    class Meta:
        model = Tag
        fields=['id', 'name', 'slug']
        read_only_fields = ['slug']
    #readonly fields cannot be modified directly through the serializer.
    #it’s generated automatically by the system.
    """ example: 
    {
    "id": 1,
    "name": "Python",
    "slug": "python"
    }
    """
        
class ArticleSerializer(serializers.ModelSerializer): #Full create/update with nested tag management.
    author_name=serializers.CharField(source='author.username', read_only=True) #pull author name
    tags=TagSerializer(source='article_tags.tag', many=True, read_only=True)
    tag_ids=serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
class Meta:
    model=Article
    fields=[
        'id','title','slug','author', 'author_name',
            'content', 'excerpt', 'status', 'created_at',
            'updated_at','published_at', 'tags','tag_ids'
            ]
    read_only_fields=[
        'slug','author','createD_at','updated_at','published_at'
    ]
    
def create(self, validated_data):
    #Removes tag_ids from validated data, pop() returns its value
    # if not found, returns empty list
    # this prevents errors during article creation
    tag_ids=validated_data.pop('tags_ids', [])
    article=Article.objects.create(**validated_data)
    
    for tag_id in tag_ids:
        try:
            tag =Tag.objects.get(id=tag_id)
            ArticleTag.objects.create(article=article, tag=tag)
        except Tag.DoesNotExist:
            pass
        
    return article    
        
def update(self, instance, validated_data):
    tag_ids = validated_data.pop('tag_ids', None) #Removes tag_ids if included.


    #Updates all other fields dynamically (setattr).
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    
    if tag_ids is not None:
        
        ArticleTag.objects.filter(article=instance).delete() #remove existing
        #adding new
        for tag_id in tag_ids:
            try:
                tag=Tag.objects.get(id=tag_id) #get the id and do the action written below
                ArticleTag.objects.create(article=instance, tag=tag)
            except Tag.DoesNotExist:
                pass
    return instance

class ArticleListSerializer(serializers.ModelSerializer): #Simplified version for listing articles efficiently.
    author_name=serializers.CharField(source='author.username', read_only=True)
    tag_count=serializers.SerializerMethodField()
    excerpt=serializers.SerializerMethodField()
    
    class Meta:
        model=Article
        fields=[
            'id','title','slug','author','author_name',
            'excerpt', 'status', 'published_at', 'tag_count'
        ]
    def get_tag_count(self, obj):
        return obj.article_tags.count() #Counts tags related to the article.
    
    
    def get_excerpt(self, obj):
        
        if obj.body: #Return first 100 characters of article body
            return obj.body[:100] + ('...' if len(obj.body) > 100 else '')
        return ""
    
    
    """ summary
    Articles → many-to-many → Tags (through ArticleTag),
    Serializer handles both read (tags) and write (tag_ids) sides
    """