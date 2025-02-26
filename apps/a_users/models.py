from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from apps.core.models import dependence, department


class Profile(models.Model):
    user_role = [(1, "citizen"), (2, "employe"), (3, "administrator")]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    displayname = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Nombre Completo"
    )
    info = models.TextField(
        null=True, blank=True, verbose_name="Információn complementaria"
    )
    role = models.IntegerField(verbose_name="Rol", choices=user_role, default=1)
    dependence = models.ForeignKey(
        dependence, on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(
        department, on_delete=models.CASCADE, null=True, blank=True
    )
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        if self.displayname:
            return self.displayname
        return self.user.username

    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return f"{settings.STATIC_URL}images/NoPhoto.png"
