from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Organization(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class UserOrganization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username + " <> " + self.organization.name


class OrganizationInvite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=128)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    selected_organization = models.ForeignKey(
        Organization,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        default=None)
    display_mode = models.IntegerField(choices=((1, 'light'), (2, 'dark')), default=1)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
