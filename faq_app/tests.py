from django.test import TestCase
from .models import FAQ

# Create your tests here.


class FAQTestCase(TestCase):
    def test_faq_translation(self):
        faq = FAQ.objects.create(question="What is Django?", answer="Django is a web framework.")
        self.assertEqual(faq.get_translated_question('hi'), faq.question_hi)