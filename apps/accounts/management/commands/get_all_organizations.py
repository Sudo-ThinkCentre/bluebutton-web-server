from ...models import UserProfile
from django.core.management.base import BaseCommand


def list_organization_names():
    orgs = []
    user_profiles = UserProfile.objects.all()
    for up in user_profiles:
        if up.organization_name:
            orgs.append(up.organization_name)
    return orgs


class Command(BaseCommand):
    help = 'List all organization names '

    def handle(self, *args, **options):
        orgs = list_organization_names()
        for i in orgs:
            print(i)
        if not orgs:
            print('No organizations to display.')
