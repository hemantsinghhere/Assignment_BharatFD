from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache
from googletrans import Translator


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
                
                faq.question = faq.get_translated_question(lang)

                
                if lang != "en":  
                    try:
                        translated_answer = translator.translate(faq.answer, dest=lang).text
                        faq.answer = translated_answer
                    except Exception as e:
                        
                        print(f"Translation failed: {e}")
                        faq.answer = faq.answer

            cache.set(cache_key, queryset, timeout=60 * 15)  

        return queryset


