# projects/language_utils.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Project

VALID_LANGUAGE_CODES = {code for code, _ in Project.PROGRAMMING_LANGUAGE_CHOICES}


def normalize_project_languages(attrs, require_languages=True):
    languages = attrs.get('languages')
    language = attrs.get('language')

    if languages is not None:
        if not isinstance(languages, list) or len(languages) == 0:
            raise serializers.ValidationError({
                'languages': _('يجب اختيار لغة واحدة على الأقل')
            })

        unique_languages = []
        seen = set()
        for lang in languages:
            if lang not in VALID_LANGUAGE_CODES:
                raise serializers.ValidationError({
                    'languages': _('لغة البرمجة المحددة غير صالحة: %(lang)s') % {'lang': lang}
                })
            if lang not in seen:
                seen.add(lang)
                unique_languages.append(lang)

        attrs['languages'] = unique_languages
        attrs['language'] = unique_languages[0]
    elif language:
        if language not in VALID_LANGUAGE_CODES:
            raise serializers.ValidationError({
                'language': _('لغة البرمجة المحددة غير صالحة')
            })
        attrs['languages'] = [language]
    elif require_languages:
        raise serializers.ValidationError({
            'languages': _('يجب اختيار لغة واحدة على الأقل')
        })

    return attrs
