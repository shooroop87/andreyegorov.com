from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings

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
    from portfolio.models import Project
    
    context = {
        'page_title': 'Projects',
        'meta_description': 'Portfolio of web development and data analytics projects.',
        'projects': Project.objects.filter(is_published=True),
    }
    return render(request, 'pages/projects.html', context)

# Блог
def blog(request):
    from blog.models import Article
    
    context = {
        'page_title': 'Blog',
        'meta_description': 'Articles about web development and data analytics.',
        'articles': Article.objects.filter(is_published=True),
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

# Статья
def article_detail(request, slug):
    from blog.models import Article
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'pages/article.html', {'article': article})


@require_POST
def contact_submit(request):
    try:
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        message = request.POST.get('message', '')
        
        subject = f'Portfolio Contact: {name}'
        body = f"""
New message from portfolio:

Name: {name}
Email: {email}
Phone: {phone}
Company: {company}

Message:
{message}
        """
        
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)