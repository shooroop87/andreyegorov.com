from django.shortcuts import render
from django.views.decorators.cache import cache_page

# Главная страница
def index(request):
    context = {
        'page_title': 'Home',
        'meta_description': 'Andrey Egorov - Full-Stack Developer, Data & Product Analyst based in Milan.',
    }
    return render(request, 'index.html', context)

# О себе
def about(request):
    context = {
        'page_title': 'About',
        'meta_description': 'Learn more about Andrey Egorov - professional background, skills, and experience.',
    }
    return render(request, 'pages/about.html', context)

# Проекты
def projects(request):
    context = {
        'page_title': 'Projects',
        'meta_description': 'Portfolio of web development and data analytics projects by Andrey Egorov.',
        # Здесь можно добавить список проектов из БД
        # 'projects': Project.objects.filter(published=True).order_by('-created_at')
    }
    return render(request, 'pages/projects.html', context)

# Блог
def blog(request):
    context = {
        'page_title': 'Blog',
        'meta_description': 'Articles and insights about web development, data analytics, and technology.',
        # Здесь можно добавить список постов
        # 'posts': BlogPost.objects.filter(published=True).order_by('-published_at')[:10]
    }
    return render(request, 'pages/blog.html', context)

# Контакты
def contacts(request):
    context = {
        'page_title': 'Contact',
        'meta_description': 'Get in touch with Andrey Egorov for project inquiries and collaboration.',
        'email': 'job@andreyegorov.com',
        'linkedin': 'https://linkedin.com/in/andreyegorov',
        'telegram': 'https://t.me/egorovvmilane',
        'whatsapp': 'https://api.whatsapp.com/send?phone=393458856224',
    }
    return render(request, 'pages/contacts.html', context)