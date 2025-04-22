from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json
from .models import *
from django.template.loader import get_template


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"].id
        self.group_name = f"notifications_{self.user}"

        if self.scope["user"].is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name
            )
            self.accept()
            return
        else:
            self.close()

    def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name, self.channel_name
            )

    def recibir_notificacion(self, event):
        print("contesto:")
        html = get_template("notification/notification.html").render(
            context={"notification": event["message"]}
        )
        self.send(text_data=html)
