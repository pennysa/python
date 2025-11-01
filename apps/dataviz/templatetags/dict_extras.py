# apps/dataviz/templatetags/dict_extras.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """允許模板用 dict[key] 方式取值"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")
    return ""
