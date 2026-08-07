from telekom.models import AdminBroadcastMessage


def admin_broadcast_message(request):
    return {'admin_broadcast_message': AdminBroadcastMessage.objects.first()}
