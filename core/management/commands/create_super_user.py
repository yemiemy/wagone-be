import logging


from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates super user if no staff user is found"

    def handle(self, *args, **options):
        from accounts.models import User

        # check if admin doesn't exists
        if not User.objects.filter(is_staff=True).exists():
            logger.info(
                "WagOne admin does not exist. Creating WagOne admin..."
            )
            admin = User.objects.create_superuser(
                username=settings.DJANGO_SU_NAME,
                email=settings.DJANGO_SU_EMAIL,
                password=settings.DJANGO_SU_PASSWORD,
            )
            logger.info("Created WagOne admin {}".format(admin))
