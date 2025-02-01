from django.db import models

# Create your models here.

from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField("Question")
    answer = RichTextField("Answer")
    question_hi = models.TextField("Question (Hindi)", blank=True, null=True)
    question_bn = models.TextField("Question (Bengali)", blank=True, null=True)

    def get_translated_question(self, lang):
        """Retrieve the translated question based on the language."""
        translations = {
            'hi': self.question_hi,
            'bn': self.question_bn,
        }
        return translations.get(lang, self.question)  # Fallback to English

    def save(self, *args, **kwargs):
        """Automatically translate questions when saving."""
        translator = Translator()
        if not self.question_hi:
            self.question_hi = translator.translate(self.question, dest='hi').text
        if not self.question_bn:
            self.question_bn = translator.translate(self.question, dest='bn').text
        super().save(*args, **kwargs)