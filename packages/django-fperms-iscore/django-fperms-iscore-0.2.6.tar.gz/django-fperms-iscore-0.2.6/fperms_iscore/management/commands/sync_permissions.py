from django.core.management.base import BaseCommand

from chamber.utils.decorators import translation_activate_block

from is_core.site import get_cores

from fperms import get_perm_model

from fperms_iscore import enums
from fperms_iscore.permissions import permissions


Perm = get_perm_model()


class Command(BaseCommand):

    help = 'Synchronize fperms permissions with database'

    @translation_activate_block
    def handle(self, *args, **kwargs):
        for permission in permissions.values():
            Perm.objects.update_or_create(
                type=enums.PERM_TYPE_CORE,
                codename=permission.name,
                defaults={
                    'name': permission.verbose_name
                }
            )
        self.stdout.write('{} FPerm permissions was updated'.format(len(permissions)))
