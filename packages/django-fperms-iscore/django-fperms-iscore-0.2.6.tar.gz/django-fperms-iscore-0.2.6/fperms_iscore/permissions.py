from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q

from fperms import get_perm_model

from fperms_iscore import enums

from is_core.auth.permissions import IsAuthenticated


Perm = get_perm_model()


permissions = {}


class FPermPermission(IsAuthenticated):

    def __init__(self, name, verbose_name=None, register=True):
        """
        :param name: name of the permission stored as codename in `Perm` model
        :param verbose_name: verbose name of the permission
        """
        self.name = name
        self.verbose_name = verbose_name
        if register:
            self._register()

    def _register(self):
        if self.name in permissions:
            raise ImproperlyConfigured('Duplicite permission with name {}'.format(self.name))
        permissions[self.name] = self

    def _get_cache(self, request):
        request._permissions_cache = getattr(request, '_permissions_cache', {})
        return request._permissions_cache

    def _add_to_cache(self, request, obj, has_perm):
        key = (request.user.pk, obj.pk if obj else None)
        self._get_cache(request).setdefault(self.name, {})[key] = has_perm

    def _get_perm(self, obj):
        """
        Return permission according to permission name and object ID (if permission is related to some object)
        if permission is not found the None value is returned.
        :param obj: model instance of the Core
        :return: `Perm` object or None
        """
        perms = Perm.objects.filter(
            Q(
                type=enums.PERM_TYPE_CORE,
                codename=self.name,
            ),
            Q(
                Q(object_id=obj.pk if obj else None) |
                Q(object_id=None)
            )
        )
        try:
            return perms.get()
        except Perm.DoesNotExist:
            return None

    def has_permission(self, name, request, view, obj=None):
        """
        Return `True` if user has set permission of is superuser
        """
        if not super().has_permission(name, request, view, obj):
            return False
        else:
            try:
                return self._get_cache(request)[self.name][(request.user.pk, obj.pk if obj else None)]
            except KeyError:
                 has_perm = request.user.perms.has_perm(self._get_perm(obj=obj))
                 self._add_to_cache(request, obj, has_perm)
                 return has_perm
