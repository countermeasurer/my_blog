from django import template
from django.db.models import Count
from taggit.models import Tag

register = template.Library()


@register.simple_tag
def popular_tags():
    tags = Tag.objects.annotate(num_times=Count('article')).order_by('-num_times')
    tags_list = list(tags.values('name', 'num_times', 'slug'))
    return tags_list
