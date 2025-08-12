from django.core.exceptions import PermissionDenied


def super_admin_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_super_admin():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped


def homecell_or_super_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_super_admin() or request.user.is_homecell_pastor()):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped


def ministry_or_super_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_super_admin() or request.user.is_ministry_leader()):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped