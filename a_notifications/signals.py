from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from core.models import TrackingProcedure, Notification
from a_users.models import Profile

@receiver(post_save, sender=TrackingProcedure)
def crear_notificacion(sender, instance, created, **kwargs):
    if created:
        #ser.profile.department)
        print("llegue al signal")
        print(instance.from_department.id)
        usuarios = User.objects.filter(profile__department__id=instance.from_department.id)
        channel_layer = get_channel_layer()
        for usuario in usuarios:
            Notification.objects.create(
                user=usuario,
                message=f"Gestión asignada: {instance.procedure}",
            )
            group_name=f"notifications_{usuario.id}"
            event = {
            "type": "recibir_notificacion",
            "message": f"Gestión asignada: {instance.procedure}",
            }
            async_to_sync(channel_layer.group_send)(group_name,event)
            
