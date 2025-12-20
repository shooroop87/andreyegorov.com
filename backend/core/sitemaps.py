from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import override as translation_override


class CompleteSitemap(Sitemap):

    protocol = "https"

    def __init__(self):
        self.languages = [lang[0] for lang in settings.LANGUAGES]

    def items(self):
        """Возвращает кортежи (url_name, language_code)"""
        items = []
        url_names = [
            "index",
            "about",
            "projects",
            "blog",
            "contacts",
        ]

        for url_name in url_names:
            for lang_code in self.languages:
                items.append((url_name, lang_code))

        return items

    def location(self, item):
        url_name, lang_code = item

        with translation_override(lang_code):
            try:
                url = reverse(url_name)

                if lang_code == settings.LANGUAGE_CODE:
                    return url
                else:
                    if not url.startswith(f"/{lang_code}/"):
                        url = f"/{lang_code}{url}"
                    return url

            except Exception as e:
                print(f"Ошибка генерации URL для {url_name} на языке {lang_code}: {e}")
                return None

    def lastmod(self, item):
        return timezone.now()

    def priority(self, item):
        url_name, lang_code = item

        if url_name == "index":
            return 1.0
        elif url_name in ["about", "projects"]:
            return 0.8
        elif url_name in ["blog", "contacts"]:
            return 0.7
        else:
            return 0.5

    def changefreq(self, item):
        url_name, lang_code = item

        if url_name == "index":
            return "weekly"
        elif url_name == "blog":
            return "daily"
        else:
            return "monthly"