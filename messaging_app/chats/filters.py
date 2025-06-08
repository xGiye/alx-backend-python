import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']
