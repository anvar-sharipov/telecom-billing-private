import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

# Строки вида "Поле изменено с X на Y" (и старый вариант "Изменения Hoz/Bud c X на Y" с латинской "c")
_CHANGE_LINE_RE = re.compile(r'^(?P<field>.+?)\s+(?:изменено\s+с|c)\s+(?P<old>.*?)\s+на\s+(?P<new>.*)$')


@register.filter
def format_baza_change(comment):
    if not comment:
        return ''

    parts = []
    for raw_line in comment.split('\n'):
        line = raw_line.strip()
        if not line:
            continue

        if line.lower().startswith('изменения:'):
            continue

        if line.lower().startswith('комментарий'):
            comment_text = escape(line[len('комментарий'):].strip())
            parts.append(
                '<div class="baza-change-comment">'
                '<span class="baza-change-comment-label">Комментарий:</span> '
                f'{comment_text}</div>'
            )
            continue

        match = _CHANGE_LINE_RE.match(line)
        if match:
            field = escape(match.group('field').strip())
            old = escape(match.group('old').strip()) or '<i>пусто</i>'
            new = escape(match.group('new').strip()) or '<i>пусто</i>'
            parts.append(
                '<div class="baza-change-row">'
                f'<span class="baza-change-field">{field}</span>: '
                f'<span class="baza-change-old">{old}</span>'
                ' &rarr; '
                f'<span class="baza-change-new">{new}</span>'
                '</div>'
            )
        else:
            parts.append(f'<div class="baza-change-plain">{escape(line)}</div>')

    return mark_safe(f'<div class="baza-change-list">{"".join(parts)}</div>')
