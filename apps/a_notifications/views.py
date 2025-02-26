from django.shortcuts import render

# Create your views here.
def notification_view(request):
    return render(request, "notification/btn_notification.html")