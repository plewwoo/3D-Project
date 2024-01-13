from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.html import mark_safe


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    tel = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def profileName(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    profileName.short_description = 'Name'

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="/media/%s" width="100" height="100" style="object-fit: cover">' % (self.image))
        else:
            return self.user.first_name[0]

    image_tag.short_description = 'ProfilePic'

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Models(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    model = models.FileField(upload_to='model', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.name)

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"
