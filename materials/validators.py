from django.core.exceptions import ValidationError

def validate_youtube_url(value):
    """Проверяет ссылку"""
    if value:
        if 'youtube.com' not in value and 'youtu.be' not in value:
            raise ValidationError('Разрешены только ссылки на YouTube')