from rest_framework import serializers

from django.utils import timezone


def validate_year(value):
        current_year = timezone.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                'Укажите год создания произведения.'
            )
        return value