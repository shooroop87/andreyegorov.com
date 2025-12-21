from django.db import models
from django.urls import reverse


class Project(models.Model):
    title = models.CharField('Title', max_length=200)
    slug = models.SlugField('Slug', unique=True)
    subtitle = models.CharField('Subtitle', max_length=300, blank=True)
    description = models.TextField('Description', blank=True)
    
    # Изображение
    image = models.ImageField('Image', upload_to='projects/', blank=True)
    
    # Теги (простой вариант через CharField)
    tags = models.CharField('Tags', max_length=300, help_text='Comma separated: Python, Django, React')
    
    # Ссылки
    url = models.URLField('Project URL', blank=True)
    github_url = models.URLField('GitHub URL', blank=True)
    
    # Мета
    is_published = models.BooleanField('Published', default=True)
    is_featured = models.BooleanField('Featured', default=False)
    order = models.PositiveIntegerField('Order', default=0)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        """Возвращает список тегов"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]