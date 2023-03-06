import secrets

from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Organization(models.Model):
    name = models.CharField(max_length=64, help_text="Usually the name of your business or website")
    readonly_fields = ('id',)
    auto_add_user = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserOrganization(models.Model):
    ADMIN = 4
    EDITOR = 3
    CREATOR = 2
    RUNNER = 1
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    perm_admin = models.BooleanField(default=True)
    perm_database_edit = models.BooleanField(default=True)
    perm_query_edit = models.BooleanField(default=True)
    perm_query_create = models.BooleanField(default=True)

    user_level = models.IntegerField(
        choices=(
            (ADMIN, 'admin'),      # add / edit databases, send invitations, edit user permissions
                                   # admin queries are executed with the admin db user
            (EDITOR, 'editor'),    # edit / delete other's queries, alter DBs
            (CREATOR, 'creator'),  # create queries, edit / delete their own queries
            (RUNNER, 'runner'),    # run queries

        ),
        default=ADMIN,
        blank=False)

    def is_admin(self):
        return self.user_level == self.ADMIN

    def is_editor(self):
        return self.user_level == self.EDITOR

    def is_creator(self):
        return self.user_level == self.CREATOR

    def can_alter_db(self):
        return self.is_editor() or self.is_admin()

    def can_create_query(self):
        return self.is_creator() or self.is_editor() or self.is_admin()

    def can_edit_query(self, query):
        return (self.is_creator() and query.author == self.user) or self.is_editor() or self.is_admin()


    def __str__(self):
        return self.user.username + " <> " + self.organization.name


# When a user signs up with a specific email, they will be invited to the organization
class Invitation(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # who made the invitation
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=1)
    email = models.CharField(max_length=128, help_text="The email of the person you'd like to invite")
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.creator.username + ", " + self.organization.name + ": " + self.email


class Referral(models.Model):
    ref_code = models.CharField(max_length=128,
                                blank=True,
                                default=None,
                                null=True,
                                unique=True,
                                help_text="a url slug like 'youtube_parameterized_queries'")
    title = models.CharField(max_length=128)
    url = models.CharField(max_length=128,
                           blank=True,
                           default=None,
                           help_text="where this referral is coming from")
    description = models.TextField(blank=True,
                                   default=None, )
    site = models.CharField(
        max_length=128,
        choices=(
            ('youtube', 'youtube'),
            ('google ads', 'google ads'),
            ('linkedin', 'linkedin'),
            ('other', 'other'),
        ),
        default='other',
        blank=True)
    visit_count = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    selected_organization = models.ForeignKey(
        Organization,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=None)
    display_mode = models.IntegerField(choices=((1, 'light'), (2, 'dark'), (3, 'synthwave')), default=3, blank=True)
    referral = models.ForeignKey(Referral, null=True, default=None, on_delete=models.DO_NOTHING)
    accept_terms_of_service = models.BooleanField(
        default=False,
        help_text="This software is released under the <a href='https://www.apache.org/licenses/LICENSE-2.0'>Apache 2.0 license</a>.  By checking this, you agree to those terms."
    )
    api_key = models.CharField(max_length=32, null=True, default=None)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def reset_api_key(self):
        self.api_key = secrets.token_urlsafe(16)
        self.save()
