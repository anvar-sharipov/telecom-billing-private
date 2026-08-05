from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .models import (ATTACHMENT_MAX_SIZE, Conversation, Message, MessageRead,
                     OnlineSession, TypingStatus, UserActivity)

User = get_user_model()

MAX_TEXT_LEN = 2000
PAGE_SIZE = 50
LOGIN_URL = 'user-login'


def _full_name(u):
    return f'{u.first_name} {u.last_name}'.strip() or u.username


def _initials(name):
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return name[:2].upper()


def _conv_display(conv, me):
    """Имя беседы для пользователя: имя группы либо имя собеседника."""
    if conv.type == Conversation.TYPE_GROUP:
        return conv.name or f'Группа #{conv.pk}'
    other = next((p for p in conv.participants.all() if p.pk != me.pk), None)
    return _full_name(other) if other else '—'


def _get_my_conv(request, conv_id):
    try:
        return Conversation.objects.prefetch_related('participants').get(
            pk=int(conv_id), participants=request.user)
    except (ValueError, TypeError, Conversation.DoesNotExist):
        return None


def _msg_to_dict(m, me):
    has_att = bool(m.attachment) and not m.is_deleted
    return {
        'id': m.id,
        'sender_id': m.sender_id,
        'sender': _full_name(m.sender) if m.sender else '—',
        'initials': _initials(_full_name(m.sender)) if m.sender else '—',
        'text': '' if m.is_deleted else m.text,
        'is_deleted': m.is_deleted,
        'time': m.created_at.strftime('%d.%m.%Y %H:%M'),
        # прочитано ли моё сообщение кем-то (для ✓✓)
        'read': any(r.user_id != m.sender_id for r in m.reads.all()),
        'attachment_url': m.attachment.url if has_att else None,
        'attachment_name': m.attachment_name if has_att else None,
        'attachment_size': m.attachment_size if has_att else None,
        'is_image': has_att and (m.attachment_content_type or '').startswith('image/'),
    }


def _last_msg_preview(last):
    if last.text:
        return last.text[:80]
    if last.attachment:
        if (last.attachment_content_type or '').startswith('image/'):
            return '🖼 Фото'
        return ('📎 ' + (last.attachment_name or 'Файл'))[:80]
    return ''


@login_required(login_url=LOGIN_URL)
def chat_page(request):
    users = User.objects.filter(is_active=True).exclude(pk=request.user.pk).order_by('username')
    users_data = [
        {'id': u.pk, 'name': _full_name(u), 'username': u.username, 'initials': _initials(_full_name(u))}
        for u in users
    ]
    return render(request, 'chat/chat.html', {'chat_users': users_data})


@login_required(login_url=LOGIN_URL)
@require_GET
def conversations_list(request):
    me = request.user
    data = []
    convs = me.chat_conversations.all().prefetch_related('participants')
    for c in convs:
        last = c.messages.select_related('sender').order_by('-id').first()
        unread = c.messages.filter(is_deleted=False).exclude(sender=me).exclude(reads__user=me).count()
        name = _conv_display(c, me)
        data.append({
            'id': c.pk,
            'type': c.type,
            'name': name,
            'initials': _initials(name),
            'unread': unread,
            'last_id': last.id if last else 0,
            'last_message': None if last is None else {
                'sender_id': last.sender_id,
                'sender': _full_name(last.sender) if last.sender else '—',
                'text': '' if last.is_deleted else _last_msg_preview(last),
                'is_deleted': last.is_deleted,
                'time': last.created_at.strftime('%d.%m %H:%M'),
            },
        })
    data.sort(key=lambda x: x['last_id'], reverse=True)
    return JsonResponse({'conversations': data})


@login_required(login_url=LOGIN_URL)
@require_POST
def conversation_create(request):
    me = request.user
    conv_type = request.POST.get('type')
    name = (request.POST.get('name') or '').strip()
    try:
        ids = [int(i) for i in request.POST.getlist('participant_ids')]
    except (ValueError, TypeError):
        return JsonResponse({'error': 'bad participants'}, status=400)

    others = list(User.objects.filter(pk__in=ids, is_active=True).exclude(pk=me.pk))
    if not others:
        return JsonResponse({'error': 'no participants'}, status=400)

    if conv_type == Conversation.TYPE_DIRECT:
        other = others[0]
        # личная беседа с этим человеком уже есть — возвращаем её
        existing = (Conversation.objects.filter(type=Conversation.TYPE_DIRECT, participants=me)
                    .filter(participants=other).first())
        if existing:
            return JsonResponse({'id': existing.pk})
        conv = Conversation.objects.create(type=Conversation.TYPE_DIRECT)
        conv.participants.set([me, other])
    elif conv_type == Conversation.TYPE_GROUP:
        if not name:
            return JsonResponse({'error': 'name required'}, status=400)
        conv = Conversation.objects.create(type=Conversation.TYPE_GROUP, name=name[:255])
        conv.participants.set([me] + others)
    else:
        return JsonResponse({'error': 'bad type'}, status=400)
    return JsonResponse({'id': conv.pk})


@login_required(login_url=LOGIN_URL)
@require_GET
def chat_messages(request):
    conv = _get_my_conv(request, request.GET.get('conv'))
    if conv is None:
        return JsonResponse({'error': 'bad conversation'}, status=400)
    try:
        after = int(request.GET.get('after', 0))
    except (ValueError, TypeError):
        after = 0

    qs = conv.messages.select_related('sender').prefetch_related('reads')
    if after > 0:
        msgs = list(qs.filter(id__gt=after)[:PAGE_SIZE])
    else:
        msgs = list(reversed(qs.order_by('-id')[:PAGE_SIZE]))

    # до какого id мои сообщения в этой беседе кем-то прочитаны (для ✓✓ без перезагрузки)
    read_up_to = conv.messages.filter(
        sender=request.user, reads__isnull=False).aggregate(m=Max('id'))['m'] or 0

    # кто сейчас печатает (статус живёт 5 секунд)
    cutoff = timezone.now() - timedelta(seconds=5)
    typing = [
        _full_name(t.user)
        for t in conv.typing.select_related('user').filter(updated_at__gte=cutoff).exclude(user=request.user)
    ]

    return JsonResponse({
        'messages': [_msg_to_dict(m, request.user) for m in msgs],
        'read_up_to': read_up_to,
        'typing': typing,
    })


@login_required(login_url=LOGIN_URL)
@require_POST
def chat_send(request):
    conv = _get_my_conv(request, request.POST.get('conv'))
    if conv is None:
        return JsonResponse({'error': 'bad conversation'}, status=400)
    text = (request.POST.get('text') or '').strip()
    f = request.FILES.get('file')
    if not text and not f:
        return JsonResponse({'error': 'empty'}, status=400)
    if f is not None and f.size > ATTACHMENT_MAX_SIZE:
        return JsonResponse({'error': 'Файл слишком большой. Максимум 20 МБ.'}, status=400)

    m = Message(conversation=conv, sender=request.user, text=text[:MAX_TEXT_LEN])
    if f is not None:
        m.attachment = f
        m.attachment_name = f.name[:255]
        m.attachment_size = f.size
        m.attachment_content_type = (f.content_type or '')[:100]
    m.save()
    return JsonResponse({'message': _msg_to_dict(m, request.user)})


@login_required(login_url=LOGIN_URL)
@require_POST
def chat_read(request):
    conv = _get_my_conv(request, request.POST.get('conv'))
    if conv is None:
        return JsonResponse({'error': 'bad conversation'}, status=400)
    try:
        last_id = int(request.POST.get('last_id', 0))
    except (ValueError, TypeError):
        last_id = 0
    if last_id > 0:
        unread = conv.messages.filter(id__lte=last_id).exclude(
            sender=request.user).exclude(reads__user=request.user)
        for m in unread:
            try:
                MessageRead.objects.get_or_create(message=m, user=request.user)
            except IntegrityError:
                pass
    return JsonResponse({'ok': True})


@login_required(login_url=LOGIN_URL)
@require_POST
def message_delete(request):
    try:
        m = Message.objects.get(pk=int(request.POST.get('id')), sender=request.user)
    except (ValueError, TypeError, Message.DoesNotExist):
        return JsonResponse({'error': 'not found'}, status=400)
    m.is_deleted = True
    m.save(update_fields=['is_deleted'])
    return JsonResponse({'ok': True})


@login_required(login_url=LOGIN_URL)
@require_POST
def chat_typing(request):
    conv = _get_my_conv(request, request.POST.get('conv'))
    if conv is None:
        return JsonResponse({'error': 'bad conversation'}, status=400)
    TypingStatus.objects.update_or_create(conversation=conv, user=request.user)
    return JsonResponse({'ok': True})


SESSION_GAP_SECONDS = 180


@login_required(login_url=LOGIN_URL)
@require_GET
def chat_unread(request):
    # для бейджа в навбаре на всех страницах; заодно отмечаем активность (онлайн-статус)
    UserActivity.objects.update_or_create(user=request.user)
    # и ведём историю онлайн-сессий
    now = timezone.now()
    last = OnlineSession.objects.filter(user=request.user).order_by('-id').first()
    if last and (now - last.last_ping).total_seconds() <= SESSION_GAP_SECONDS:
        last.last_ping = now
        last.save(update_fields=['last_ping'])
    else:
        OnlineSession.objects.create(user=request.user)
    total = (Message.objects.filter(conversation__participants=request.user, is_deleted=False)
             .exclude(sender=request.user).exclude(reads__user=request.user).count())
    return JsonResponse({'total': total})


# ===== список пользователей (онлайн/этрапы) =====

ONLINE_TIMEOUT_SECONDS = 60
# группы вида <Этрап>_<Отдел>: Dashoguz_Kassa, S.A.Nyyazow_MTB ...
DEPT_SUFFIXES = {'MTB', 'Kassa', 'MB', '071', 'Internet', 'SHB'}


def _parse_group(name):
    """'Dashoguz_Kassa' -> ('Dashoguz', 'Kassa'); служебные группы -> (None, None)."""
    if '_' in name:
        prefix, suffix = name.rsplit('_', 1)
        if suffix in DEPT_SUFFIXES:
            return prefix, suffix
    return None, None


@login_required(login_url=LOGIN_URL)
def users_page(request):
    return render(request, 'chat/users.html')


@login_required(login_url=LOGIN_URL)
@require_GET
def users_data(request):
    cutoff = timezone.now() - timedelta(seconds=ONLINE_TIMEOUT_SECONDS)
    activity = {a.user_id: a.last_seen for a in UserActivity.objects.all()}

    data = []
    qs = User.objects.filter(is_active=True).prefetch_related('groups').order_by('username')
    for u in qs:
        etraps, otdels = set(), set()
        for g in u.groups.all():
            etrap, otdel = _parse_group(g.name)
            if etrap:
                etraps.add(etrap)
                otdels.add(otdel)
        last_seen = activity.get(u.pk)
        name = _full_name(u)
        data.append({
            'id': u.pk,
            'name': name,
            'username': u.username,
            'initials': _initials(name),
            'etraps': sorted(etraps),
            'otdels': sorted(otdels),
            'online': last_seen is not None and last_seen >= cutoff,
            'last_seen': last_seen.strftime('%d.%m.%Y %H:%M') if last_seen else None,
        })

    all_etraps = sorted({e for row in data for e in row['etraps']})
    return JsonResponse({'users': data, 'etraps': all_etraps})


@login_required(login_url=LOGIN_URL)
def users_history_page(request):
    return render(request, 'chat/users_history.html')


MONTH_NAMES_RU = ['', 'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
                  'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']


@login_required(login_url=LOGIN_URL)
@require_GET
def users_history_data(request):
    try:
        days = max(1, min(366, int(request.GET.get('days', 7))))
    except (ValueError, TypeError):
        days = 7
    # для длинных периодов (например "Год") группируем по месяцам —
    # 365 дневных столбиков на графике нечитаемы
    monthly = days > 31
    now = timezone.now()
    start = (now - timedelta(days=days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)

    sel_user = None
    try:
        uid = int(request.GET.get('user') or 0)
        if uid:
            sel_user = User.objects.filter(pk=uid).first()
    except (ValueError, TypeError):
        pass

    sessions = (OnlineSession.objects.filter(last_ping__gte=start)
                .select_related('user').order_by('started_at'))

    totals = {}  # user_id -> {seconds, count, last}
    for s in sessions:
        st = max(s.started_at, start)
        en = min(s.last_ping, now)
        dur = max(0.0, (en - st).total_seconds())
        t = totals.setdefault(s.user_id, {'seconds': 0.0, 'count': 0, 'last': None})
        t['seconds'] += dur
        t['count'] += 1
        if t['last'] is None or s.last_ping > t['last']:
            t['last'] = s.last_ping

    users_out = []
    for u in User.objects.filter(is_active=True).order_by('username'):
        t = totals.get(u.pk)
        name = _full_name(u)
        users_out.append({
            'id': u.pk,
            'name': name,
            'username': u.username,
            'initials': _initials(name),
            'seconds': int(t['seconds']) if t else 0,
            'sessions': t['count'] if t else 0,
            'last_seen': t['last'].strftime('%d.%m.%Y %H:%M') if t and t['last'] else None,
        })
    users_out.sort(key=lambda x: -x['seconds'])

    # детализация по одному пользователю: по дням (или месяцам) + список сессий
    detail = None
    if sel_user:
        bucket_totals = {}
        if monthly:
            y, m = start.year, start.month
            while (y, m) <= (now.year, now.month):
                bucket_totals[(y, m)] = 0.0
                m += 1
                if m > 12:
                    m = 1
                    y += 1
        else:
            for i in range(days):
                bucket_totals[(start + timedelta(days=i)).date()] = 0.0

        sess_list = []
        for s in sessions:
            if s.user_id != sel_user.pk:
                continue
            st = max(s.started_at, start)
            en = min(s.last_ping, now)
            dur = max(0.0, (en - st).total_seconds())
            key = (st.year, st.month) if monthly else st.date()
            if key in bucket_totals:
                bucket_totals[key] += dur
            sess_list.append({
                'start': st.strftime('%d.%m.%Y %H:%M'),
                'end': en.strftime('%H:%M'),
                'seconds': int(dur),
            })

        if monthly:
            days_out = [{'date': MONTH_NAMES_RU[m] + ' ' + str(y), 'seconds': int(v)}
                        for (y, m), v in bucket_totals.items()]
        else:
            days_out = [{'date': d.strftime('%d.%m'), 'seconds': int(v)}
                        for d, v in bucket_totals.items()]

        detail = {
            'name': _full_name(sel_user),
            'monthly': monthly,
            'days': days_out,
            'sessions': list(reversed(sess_list))[:100],
        }

    return JsonResponse({'users': users_out, 'detail': detail, 'days': days})
