from django.contrib.admin.sites import AdminSite
from django.utils.text import capfirst
from django.views.generic import View
import inspect


def is_class_based_view(view):
    return inspect.isclass(view) and issubclass(view, View)


class AdminPlusMixin(object):
    """ Thanks To django-admin plus
        Mixin for AdminSite to allow registering custom admin views.
        https://github.com/jsocol/django-adminplus
    """

    def __init__(self):
        self.custom_views = []
        super().__init__()

    def register_view(self, path, name=None, urlname=None, visible=True,
                      view=None):
        """Add a custom admin view. Can be used as a function or a decorator.
        * `path` is the path in the admin where the view will live, e.g.
            http://example.com/admin/somepath
        * `name` is an optional pretty name for the list of custom views. If
            empty, we'll guess based on view.__name__.
        * `urlname` is an optional parameter to be able to call the view with a
            redirect() or reverse()
        * `visible` is a boolean or predicate returning one, to set if
            the custom view should be visible in the admin dashboard or not.
        * `view` is any view function you can imagine.
        Example :
        ```
        @epic_site.register_view('someview',
                         name='Some View',
                         urlname='some_view',
                         visible=False)
        def my_view(request):
            from  django.http import HttpResponse
            return HttpResponse('Custom View')```
        """

        def decorator(fn):
            if is_class_based_view(fn):
                fn = fn.as_view()
            self.custom_views.append((path, fn, name, urlname, visible))
            return fn

        if view is not None:
            decorator(view)
            return

        return decorator

    def get_urls(self):
        """Add our custom views to the admin urlconf."""
        urls = super().get_urls()
        from django.conf.urls import url
        # from .views import my_view
        for path, view, name, urlname, visible in self.custom_views:
            urls = [
                       url(r'^%s/$' % path, self.admin_view(view), name=urlname),
                   ] + urls
        return urls

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        # get each context from super
        each_ctx = super().each_context(request)

        each_ctx['custom_view_list'] = self.get_custom_view_list(request)
        each_ctx['custom_app_list'] = self.get_custom_app_list(request)
        return each_ctx

    def get_custom_app_list(self, request):
        """ Return app list for each path, replace context processor capability """
        app_list = super().get_app_list(request)
        return app_list

    def get_custom_view_list(self, request):
        """ Return list of custom view """
        custom_views = self.custom_views
        view_list = []
        for path, view, name, urlname, visible in custom_views:
            urlname = 'admin:%s' % urlname
            if callable(visible):
                visible = visible(request)
            if visible:
                if name:
                    view_list.append((path, name, urlname))
                else:
                    view_list.append((path, capfirst(view.__name__), urlname))

        # Sort views alphabetically.
        view_list.sort(key=lambda x: x[1])
        return view_list


class EpicAdmin(AdminPlusMixin, AdminSite):
    """
    Epic Admin class, create custom django admin
    """
    site_header = "Epic Administration"
    site_title = "Epic Administration"
    index_title = "Welcome to Epic Admin"


epic_site = EpicAdmin()
