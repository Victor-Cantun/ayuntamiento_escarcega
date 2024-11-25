from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.contrib import messages
from django.http import Http404
from .models import *

from .forms import *


# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    chat_messages = chat_group.chat_messages.all()
    form = ChatmessageCreateForm()
    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {"message": message, "user": request.user}
            return render(request, "chat/partials/chat_message_p.html", context)
    return render(
        request, "chat/chat.html", {"chat_messages": chat_messages, "form": form}
    )
