# config/settings.py
import io
import os
import sys
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "1ins#Zvdsecure1-1default1asdsdasdasd1$5%!#")

# DEBU
DEBUG = False

# ALLOWED_HOSTS
if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1").split()

CSRF_TRUSTED_ORIGINS = [
    "https://*.andreyegorov.com",
    "https://andreyegorov.com",
    "http://localhost",
    "http://localhost:8000",
    "http://backend-1:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
]

# Приложения
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "tinymce",
    "core",
    "blog",
    "portfolio",
    "payments"
]

# Работает в связке с django.contrib.sites
SITE_ID = 1

# Dev-only apps
if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = "backend.urls"

TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "core" / "templates",  # Основные шаблоны
            BASE_DIR / "blog" / "templates",  # Шаблоны блога
            BASE_DIR / "portfolio" / "templates",  # Шаблоны портфолио
            BASE_DIR / "templates",  # Общие шаблоны
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# ===========================================
# DATABASE - SQLite3
# ===========================================
if os.environ.get('DOCKER_ENV'):
    DB_PATH = Path("/app/data/db.sqlite3")
else:
    DB_PATH = BASE_DIR / "db.sqlite3"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DB_PATH,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_CHARSET = "utf-8"
FILE_CHARSET = "utf-8"

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("it", _("Italian")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = [BASE_DIR / "core" / "locale"]

# Parler
PARLER_LANGUAGES = {
    None: (
        {"code": "en"},
        {"code": "it"},
        {"code": "ru"},
    ),
    "default": {"fallbacks": ["en"], "hide_untranslated": False},
}

# Static & media
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "collected_static"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

FILE_UPLOAD_PERMISSIONS = 0o644  # rw-r--r--
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755  # rwxr-xr-x

# Создаем медиа-директорию если не существует
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Filer / thumbnails
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_QUALITY = 90
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "easy_thumbnails.processors.scale_and_crop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

# Кеширование
if DEBUG:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }

# Email Settings - Yandex Mail for Business
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "job@andreyegorov.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = "Andrey Egorov <job@andreyegorov.com>"
CONTACT_EMAIL = "job@andreyegorov.com"

# Payments
TBANK_TERMINAL_KEY = os.getenv('TBANK_TERMINAL_KEY', '')
TBANK_SECRET_KEY = os.getenv('TBANK_SECRET_KEY', '')

# Misc
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
        },
    },
    "root": {"handlers": ["console"], "level": "ERROR"},
    "loggers": {
        "django": {"level": "ERROR", "handlers": ["console"], "propagate": False},
    },
}

# stdout fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ===================== DJANGO TINYMCE =====================
TINYMCE_JS_URL = "/static/tinymce/tinymce.min.js"
TINYMCE_COMPRESSOR = False
TINYMCE_SPELLCHECKER = False


# Основная конфигурация (аналог CKEditor 5 'default')
TINYMCE_DEFAULT_CONFIG = {
    "height": 800,
    "width": "auto",
    "menubar": "file edit view insert format tools table",
    "plugins": """
        advlist autolink lists link image charmap preview anchor searchreplace 
        visualblocks code fullscreen insertdatetime media table code 
        help wordcount table lists emoticons codesample nonbreaking pagebreak template
    """,
    "toolbar": """
        undo redo | styles | bold italic underline strikethrough | 
        forecolor backcolor | alignleft aligncenter alignright alignjustify |
        bullist numlist outdent indent | link image media swipergallery | 
        table | template | removeformat code fullscreen help
    """,
    "external_plugins": {
        "swipergallery": "/static/tinymce/plugins/swipergallery/plugin.js"
    },
    "license_key": "gpl",
    "templates": [
        {
            "title": "Accordeon (site markup)",
            "description": "JS accordion with divs",
            "content": """
        <div class="accordion -simple row y-gap-20 mt-30 js-accordion">
        <div class="col-12">
            <div class="accordion__item px-20 py-15 border-1 rounded-12">
            <div class="accordion__button d-flex items-center justify-between">
                <div class="button text-16 text-dark-1">Заголовок секции</div>
                <div class="accordion__icon size-30 flex-center bg-light-2 rounded-full">
                    <i class="icon-plus text-13"></i>
                    <i class="icon-minus text-13"></i>
                </div>
            </div>
            <div class="accordion__content">
                <div class="pt-20 ck-content">
                <p class="mt-20">Accordion content. This can include text, tables, images, etc.</p>
                </div>
            </div>
            </div>
        </div>
        </div>
            """,
        },
        {
            "title": "CTA Button",
            "description": "Centered button",
            "content": """
                <p class="mt-30" style="text-align:center">
                    <a href="#" class="button -md -dark-1 bg-accent-1 text-white" title="..." aria-label="...">
                        Call to Action
                    </a>
                </p>
            """,
        },
    ],
    # Стили для заголовков (аналог heading в CKEditor)
    "style_formats": [
        {"title": "Paragraph", "format": "p", "classes": "mt-20"},
        {"title": "Heading 1", "format": "h1"},
        {"title": "Heading 2", "format": "h2", "classes": "text-30 md:text-24"},
        {"title": "Heading 3", "format": "h3"},
        {"title": "Heading 4", "format": "h4"},
        {"title": "Heading 5", "format": "h5"},
        {"title": "Heading 6", "format": "h6"},
        {
            "title": "CTA Button",
            "selector": "a",
            "classes": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Outline",
            "selector": "a",
            "classes": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
    ],
    # Цвета (аналог fontColor в CKEditor)
    "color_map": [
        "000000",
        "Black",
        "4D4D4D",
        "Dark grey",
        "999999",
        "Grey",
        "E6E6E6",
        "Light grey",
        "FFFFFF",
        "White",
        "E64C4C",
        "Red",
        "E6804C",
        "Orange",
        "E6E64C",
        "Yellow",
        "99E64C",
        "Light green",
        "4CE64C",
        "Green",
        "4CE699",
        "Aquamarine",
        "4CE6E6",
        "Turquoise",
        "4C99E6",
        "Light blue",
        "4C4CE6",
        "Blue",
        "994CE6",
        "Purple",
        "E64CE6",
        "Magenta",
        "E64C99",
        "Pink",
    ],
    # Настройки изображений (аналог image в CKEditor)
    "image_advtab": True,
    "image_caption": True,
    "image_title": True,
    "automatic_uploads": True,
    "file_picker_types": "image",
    "images_upload_url": "/tinymce/upload/",
    "images_reuse_filename": False,
    # Таблицы (аналог table в CKEditor)
    "table_toolbar": "tableprops tabledelete | tableinsertrowbefore tableinsertrowafter tabledeleterow | tableinsertcolbefore tableinsertcolafter tabledeletecol",
    "table_appearance_options": True,
    "table_grid": True,
    "table_resize_bars": True,
    "table_default_attributes": {"border": "1"},
    "table_default_styles": {"border-collapse": "collapse", "width": "100%"},
    # Контент CSS (стили как в CKEditor)
    "content_css": [
        "/static/css/tinymce-content.css",
    ],
    "content_style": """
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #32373c;
            padding: 20px;
        }
    """,
    # Разрешенные элементы (аналог htmlSupport в TinyMCE)
    "extended_valid_elements": """
        div[class|style|data-*],
        span[class|style|data-*],
        i[class|style|data-*],
        img[class|src|alt|title|width|height|loading|data-*],
        a[href|target|rel|class|style|aria-label|aria-*|title],
        iframe[src|width|height|frameborder|allow|allowfullscreen|title|loading|referrerpolicy],
        figure[class|data-*],
        table[class|style|border|cellpadding|cellspacing],
        td[class|style|colspan|rowspan|data-label],
        th[class|style|colspan|rowspan|data-label],
        details[open|class|style|data-*|role|aria-*],
        summary[class|style|data-*|role|aria-*],
        ul[class|style|data-*],
        li[class|style|data-*],
        p[class|style|data-*|aria-*],
    """,
    "valid_elements": "+i[class|style|data-*],+span[class|style|data-*]",
    "valid_classes": {
        "div": (
            "table-responsive table-stack stack-item image-gallery gallery-grid gallery-item media accordion-panel "
            "accordion -simple row y-gap-20 mt-30 js-accordion "
            "col-12 accordion__item px-20 py-15 border-1 rounded-12 "
            "accordion__button d-flex items-center justify-between "
            "button text-16 text-dark-1 "
            "accordion__icon size-30 flex-center bg-light-2 rounded-full "
            "accordion__content pt-20 ck-content "
        ),
        "img": "gallery-image",
        "table": "compact striped lake-como-table table-normal",
        "span": (
            "stack-label stack-value stack-header "
            "icon-plus icon-minus text-13 "
            "text-accent-1 text-success text-warning "
            "badge tag"
        ),
        "i": ("icon-plus text-13 " "icon-minus text-13 "),
        "h2": "text-30 md:text-24",
        "p": "mt-20 mt-30 text-center",
        "ul": "list-disc mt-20",
        "ol": "numbered-list mt-20",
        "details": "accordion -simple row y-gap-20 mt-30 js-accordion",
        "summary": "button text-16 text-dark-1",
        "a": "cta-button cta-button-outline button -md -dark-1 bg-accent-1 text-white mt-30",
    },
    # Опции
    "branding": False,
    "promotion": False,
    "relative_urls": False,
    "remove_script_host": False,
    "convert_urls": True,
    "cleanup": False,
    "cleanup_on_startup": True,
    "paste_as_text": False,
    "paste_data_images": True,
    "browser_spellcheck": True,
    "contextmenu": "link image table",
    "verify_html": False,
}
TINYMCE_DEFAULT_CONFIG["valid_styles"] = {
    "*": "text-align,color,background-color,font-size,font-weight,text-decoration,margin,margin-left,margin-right,padding"
}
# Конфигурация для блога (аналог CKEditor 5 'blog')
TINYMCE_BLOG_CONFIG = {
    "height": 800,
    "width": "auto",
    "menubar": "file edit view insert format tools table",
    "license_key": "gpl",
    "plugins": """
        advlist autolink lists link image charmap preview anchor searchreplace 
        visualblocks code fullscreen insertdatetime media table code 
        help wordcount table lists emoticons codesample nonbreaking pagebreak
    """,
    "toolbar": """
        undo redo | styles | bold italic underline strikethrough | 
        forecolor backcolor | alignleft aligncenter alignright alignjustify |
        bullist numlist outdent indent | link image media swipergallery | 
        table | template | removeformat code fullscreen help
    """,
    "external_plugins": {
        "swipergallery": "/static/tinymce/plugins/swipergallery/plugin.js"
    },
    "templates": [
        {
            "title": "Accordeon (site markup)",
            "description": "JS accordion with divs",
            "content": """
        <div class="accordion -simple row y-gap-20 mt-30 js-accordion">
        <div class="col-12">
            <div class="accordion__item px-20 py-15 border-1 rounded-12">
            <div class="accordion__button d-flex items-center justify-between">
                <div class="button text-16 text-dark-1">Заголовок секции</div>
                <div class="accordion__icon size-30 flex-center bg-light-2 rounded-full">
                    <i class="icon-plus text-13"></i>
                    <i class="icon-minus text-13"></i>
                </div>
            </div>
            <div class="accordion__content">
                <div class="pt-20 ck-content">
                <p class="mt-20">Accordion content. This can include text, tables, images, etc.</p>
                </div>
            </div>
            </div>
        </div>
        </div>
            """,
        },
        {
            "title": "CTA Button",
            "description": "Centered button",
            "content": """
                <div style="display:flex; justify-content:center; margin-top:30px;">
                    <a href="#" class="button -md -dark-1 bg-accent-1 text-white" style="width:350px; text-align:center;">
                        Call to Action
                    </a>
                </div>
            """,
        },
    ],
    # Стили для блога
    "style_formats": [
        {"title": "Paragraph", "format": "p", "classes": "mt-20"},
        {"title": "Heading 1", "format": "h1"},
        {"title": "Heading 2", "format": "h2", "classes": "text-30 md:text-24"},
        {"title": "Heading 3", "format": "h3"},
        {"title": "Heading 4", "format": "h4"},
        {"title": "Heading 5", "format": "h5"},
        {"title": "Heading 6", "format": "h6"},
        {
            "title": "Numbered List (mt-20)",
            "selector": "ol",
            "classes": "numbered-list mt-20",
        },
        {
            "title": "CTA Button",
            "selector": "a",
            "classes": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Outline",
            "selector": "a",
            "classes": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
    ],
    # Специальные ссылки для блога (аналог link decorators в CKEditor)
    "link_class_list": [
        {"title": "Normal Link", "value": ""},
        {
            "title": "CTA Button",
            "value": "cta-button button -md -dark-1 bg-accent-1 text-white",
        },
        {
            "title": "CTA Button Outline",
            "value": "cta-button-outline button -outline-accent-1 text-accent-1",
        },
        {
            "title": "WhatsApp Button",
            "value": "whatsapp-button button -md bg-success-1 text-white",
        },
    ],
    "link_default_target": "_self",
    "target_list": [
        {"title": "Same window", "value": "_self"},
        {"title": "New window", "value": "_blank"},
    ],
    # Цвета для блога
    "color_map": [
        "000000",
        "Black",
        "4D4D4D",
        "Dark grey",
        "999999",
        "Grey",
        "E6E6E6",
        "Light grey",
        "FFFFFF",
        "White",
        "E64C4C",
        "Red",
        "E6804C",
        "Orange",
        "E6E64C",
        "Yellow",
        "99E64C",
        "Light green",
        "4CE64C",
        "Green",
        "4CE699",
        "Aquamarine",
        "4CE6E6",
        "Turquoise",
        "4C99E6",
        "Light blue",
        "4C4CE6",
        "Blue",
        "994CE6",
        "Purple",
        "E64CE6",
        "Magenta",
        "E64C99",
        "Pink",
    ],
    # Изображения
    "image_advtab": True,
    "image_caption": True,
    "automatic_uploads": True,
    "images_upload_url": "/tinymce/upload/",
    "file_picker_types": "image",
    # Таблицы с расширенными настройками
    "table_toolbar": "tableprops tabledelete | tableinsertrowbefore tableinsertrowafter tabledeleterow | tableinsertcolbefore tableinsertcolafter tabledeletecol | tablecellprops",
    "table_appearance_options": True,
    "table_advtab": True,
    "table_cell_advtab": True,
    "table_row_advtab": True,
    "table_class_list": [
        {"title": "Default", "value": ""},
        {"title": "Compact", "value": "compact"},
        {"title": "Striped", "value": "striped"},
        {"title": "Lake Como Table", "value": "lake-como-table"},
    ],
    # Медиа (аналог mediaEmbed в CKEditor)
    "media_live_embeds": True,
    "media_dimensions": True,
    "media_poster": True,
    # Контент CSS
    "content_css": "/static/css/ckeditor-content.css",
    "content_style": """
        /* WordPress-подобные стили */
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            color: #32373c;
            background: #fff;
            padding: 20px 24px;
        }
        p { margin: 0 0 1em 0; }
        p.mt-20 { margin-top: 20px; }
        h1, h2, h3, h4, h5, h6 {
            color: #23282d;
            font-weight: 600;
            margin: 1.5em 0 0.5em 0;
            line-height: 1.3;
        }
        h1 { font-size: 2.2em; margin-top: 1em; }
        h2 { font-size: 1.8em; }
        h2.text-30 { font-size: 1.875em; }
        h3 { font-size: 1.5em; }
        h4 { font-size: 1.25em; }
        h5 { font-size: 1.1em; }
        h6 { font-size: 1em; font-weight: 700; }
        a { color: #0073aa; text-decoration: none; }
        a:hover { color: #005177; text-decoration: underline; }
        blockquote {
            border-left: 4px solid #0073aa;
            margin: 1.5em 0;
            padding: 0 0 0 1em;
            font-style: italic;
            color: #666;
        }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 1em 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        table td, table th {
            border: 1px solid #e1e1e1;
            padding: 8px 12px;
            text-align: left;
        }
        table th {
            background: #f9f9f9;
            font-weight: 600;
            color: #23282d;
        }
        code {
            background: #f1f1f1;
            color: #d63384;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: Monaco, Consolas, monospace;
            font-size: 0.9em;
        }
        ul, ol { margin: 1em 0; padding-left: 2em; }
        li { margin: 0.5em 0; }
        .cta-button, .cta-button-outline, .whatsapp-button {
            display: inline-block;
            padding: 12px 30px;
            margin: 10px auto;
            text-align: center;
        }
    """,
    # Разрешенные элементы
    "extended_valid_elements": """
        div[class|style|data-*],
        span[class|style|data-*],
        i[class|style|data-*],
        img[class|src|alt|title|width|height|loading|data-*],
        a[href|target|rel|class|style|aria-label|aria-*|title],
        iframe[src|width|height|frameborder|allow|allowfullscreen|title|loading|referrerpolicy],
        figure[class|data-*],
        table[class|style|border|cellpadding|cellspacing],
        td[class|style|colspan|rowspan|data-label],
        th[class|style|colspan|rowspan|data-label],
        details[open|class|style|data-*|role|aria-*],
        summary[class|style|data-*|role|aria-*],
        ul[class|style|data-*],
        li[class|style|data-*],
        p[class|style|data-*|aria-*],
    """,
    "valid_elements": "+i[class|style|data-*],+span[class|style|data-*]",
    "valid_classes": {
        "div": (
            "table-responsive table-stack stack-item image-gallery gallery-grid gallery-item media accordion-panel "
            "accordion -simple row y-gap-20 mt-30 js-accordion "
            "col-12 accordion__item px-20 py-15 border-1 rounded-12 "
            "accordion__button d-flex items-center justify-between "
            "button text-16 text-dark-1 "
            "accordion__icon size-30 flex-center bg-light-2 rounded-full "
            "accordion__content pt-20 ck-content "
        ),
        "img": "gallery-image",
        "table": "compact striped lake-como-table table-normal",
        "span": (
            "stack-label stack-value stack-header "
            "icon-plus icon-minus text-13 "
            "text-accent-1 text-success text-warning "
            "badge tag"
        ),
        "i": ("icon-plus text-13 " "icon-minus text-13 "),
        "h2": "text-30 md:text-24",
        "p": "mt-20 mt-30 text-center",
        "ul": "list-disc mt-20",
        "ol": "numbered-list mt-20",
        "details": "accordion -simple row y-gap-20 mt-30 js-accordion",
        "summary": "button text-16 text-dark-1",
        "a": "cta-button cta-button-outline button -md -dark-1 bg-accent-1 text-white mt-30",
    },
    # Опции
    "branding": False,
    "promotion": False,
    "relative_urls": False,
    "remove_script_host": False,
    "convert_urls": True,
    "cleanup": False,
    "cleanup_on_startup": True,
    "paste_as_text": False,
    "paste_data_images": True,
    "browser_spellcheck": True,
    "contextmenu": "link image table",
    "verify_html": False,
}

# Настройки загрузки файлов (аналог CKEDITOR_5_UPLOAD_PATH)
TINYMCE_UPLOAD_PATH = "blog/content/"
TINYMCE_IMAGE_UPLOAD_ENABLED = True
TINYMCE_FILE_UPLOAD_ENABLED = True
TINYMCE_ALLOWED_FILE_TYPES = ["jpeg", "jpg", "png", "gif", "webp", "pdf", "doc", "docx"]


THUMBNAIL_FORMAT = "WEBP"
THUMBNAIL_QUALITY = 85
THUMBNAIL_PRESERVE_FORMAT = False

PAGINATE_BY = 10

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024  # 15MB

ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

IMAGE_QUALITY = 85
MAX_IMAGE_WIDTH = 1200
MAX_IMAGE_HEIGHT = 1200

# Включите кэш миниатюр
THUMBNAIL_CACHE_DIMENSIONS = True
THUMBNAIL_CACHE = "default"
