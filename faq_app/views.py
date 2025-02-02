from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache
from googletrans import Translator
import logging

# Set up logging
logger = logging.getLogger(__name__)


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        lang = self.request.query_params.get("lang", "en")
        cache_key = f"faqs_{lang}"
        queryset = cache.get(cache_key)

        if not queryset:
            queryset = super().get_queryset()
            translator = Translator()

            for faq in queryset:
                # Translate the question
                faq.question = faq.get_translated_question(lang)

                # Translate the answer (if not English)
                if lang != "en":
                    try:
                        translated_answer = translator.translate(
                            faq.answer, dest=lang
                        ).text
                        faq.answer = translated_answer
                    except Exception as e:
                        # Log the error and use the original answer
                        logger.error(f"Translation failed for FAQ ID {faq.id}: {e}")
                        faq.answer = faq.answer

            # Cache the queryset
            cache.set(cache_key, queryset, timeout=60 * 15)  # Cache for 15 minutes

        return queryset

    def perform_create(self, serializer):
    # Save the new FAQ
        faq = serializer.save()

    # Clear cache for all language versions
        cache_keys = cache.keys("faqs_*")  # Get all cached keys that match "faqs_*"
        if cache_keys:
            cache.delete_many(cache_keys)

    # Log the creation of a new FAQ
        logger.info(f"New FAQ created: ID {faq.id}, Question: {faq.question}")


