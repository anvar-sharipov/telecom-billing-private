from django.shortcuts import render, redirect
from django.contrib import messages

from telekom.models import AdminBroadcastMessage, StaffAction

from datetime import datetime


def adminMessage(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['adminMessage'] = True
    context['admin_allow'] = True

    obj, _ = AdminBroadcastMessage.objects.get_or_create(pk=1)

    if request.method == 'POST':
        obj.text = request.POST.get('text', '').strip()
        obj.is_enabled = bool(request.POST.get('is_enabled'))
        obj.updated_by = request.user.username
        obj.save()

        StaffAction.objects.create(
            user=request.user,
            comment=f'Admin message изменён, enabled={obj.is_enabled}, текст: {obj.text[:200]}, дата {datetime.now()}, изменил {request.user.username}',
            action='Another',
        )
        messages.success(request, 'Сообщение сохранено')

    context['obj'] = obj

    return render(request, 'telekom/admin_pages/adminMessage.html', context)
