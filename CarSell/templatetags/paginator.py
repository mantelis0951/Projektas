from django import template
from django.core.paginator import Paginator

register = template.Library()

@register.inclusion_tag('pagination.html')
def show_pagination_links(queryset, parameter_name='page'):
    paginator = Paginator(queryset, 3)  # Assuming 3 items per page
    return {'current_list': queryset, 'parameter_name': parameter_name}

