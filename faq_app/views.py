from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()  # Add this line
    serializer_class = FAQSerializer

    def get_queryset(self):
        lang = self.request.query_params.get("lang", "en")
        cache_key = f"faqs_{lang}"
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = super().get_queryset()
            for faq in queryset:
                faq.question = faq.get_translated_question(lang)
            cache.set(cache_key, queryset, timeout=60 * 15)  # Cache for 15 minutes
        return queryset


