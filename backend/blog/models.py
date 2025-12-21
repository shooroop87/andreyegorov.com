from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField('Title', max_length=300)
    slug = models.SlugField('Slug', unique=True)
    excerpt = models.TextField('Excerpt', max_length=500, blank=True)
    content = models.TextField('Content')
    image = models.ImageField('Image', upload_to='blog/', blank=True)
    tags = models.CharField('Tags', max_length=300, help_text='Comma separated')
    is_published = models.BooleanField('Published', default=True)
    published_at = models.DateTimeField('Published at')
    created_at = models.DateTimeField('Created', auto_now_add=True)
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]