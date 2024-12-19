from django.shortcuts import render
import secrets

def index(request):
    id = secrets.token_urlsafe(10)
    room = secrets.token_urlsafe(10)
    context = {'id': id, 'room':room}
    return render(request, "index.html",context)
