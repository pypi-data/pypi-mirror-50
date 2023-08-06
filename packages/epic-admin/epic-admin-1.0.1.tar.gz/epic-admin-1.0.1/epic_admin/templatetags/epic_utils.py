from django import template
from django.utils.text import capfirst
from django.contrib import admin

from epic_admin.admin import epic_site

register = template.Library()

class CustomRequest:
    def __init__(self, user):

        self.user = user

@register.simple_tag(takes_context=True)
def custom_app_list(context, **kwargs):
    """ Return app list owned by user """
    custom_request = CustomRequest(context['request'].user)
    app_list = epic_site.get_app_list(custom_request)
    return app_list


@register.simple_tag(takes_context=True)
def custom_views_list(context, **kwargs):
    """ Return custom view list """
    custom_views = admin.site.custom_views
    custom_list = []
    for path, view, name, urlname, visible in custom_views:
        if callable(visible):
            visible = visible(context['request'].user)
        if visible:
            if name:
                custom_list.append((path, name))
            else:
                custom_list.append((path, capfirst(view.__name__)))

    # Sort views alphabetically.
    custom_list.sort(key=lambda x: x[1])
    return custom_list
