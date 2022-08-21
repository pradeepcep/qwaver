
import factory
from factory.fuzzy import FuzzyText
from django.contrib.auth.models import User

from users.models import (
    Organization,
    Invitation,
    UserOrganization,
)


class UserFactory(factory.django.DjangoModelFactory):

    username = FuzzyText()
    email = FuzzyText(suffix="@example.com")

    class Meta:
        model = User


class OrganizationFactory(factory.django.DjangoModelFactory):

    name = factory.Sequence(lambda n: f'Organization-{n}')

    class Meta:
        model = Organization


class UserOrganizationFactory(factory.django.DjangoModelFactory):

    organization = factory.SubFactory(OrganizationFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = UserOrganization


class InviteFactory(factory.django.DjangoModelFactory):
    creator = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)
    email = FuzzyText(suffix='@example.com')

    class Meta:
        model = Invitation
