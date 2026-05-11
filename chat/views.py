"""
Views for the chat app.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Message

User = get_user_model()


def _get_conversations(user):
    """Return a list of dicts describing each unique conversation partner."""
    sent_to     = Message.objects.filter(sender=user, receiver__isnull=False).values_list('receiver_id', flat=True)
    received_from = Message.objects.filter(receiver=user).values_list('sender_id', flat=True)
    partner_ids = set(list(sent_to) + list(received_from))

    conversations = []
    for pid in partner_ids:
        try:
            other = User.objects.get(pk=pid)
        except User.DoesNotExist:
            continue

        last_msg = (
            Message.objects
            .filter(
                Q(sender=user, receiver_id=pid) |
                Q(sender_id=pid, receiver=user)
            )
            .order_by('-sent_at')
            .first()
        )
        unread = Message.objects.filter(sender_id=pid, receiver=user, is_read=False).count()
        conversations.append({
            'other_user':   other,
            'last_message': last_msg,
            'unread_count': unread,
        })

    conversations.sort(
        key=lambda c: c['last_message'].sent_at if c['last_message'] else 0,
        reverse=True,
    )
    return conversations


@login_required
def index(request):
    """Chat list — shows all private conversations."""
    return render(request, 'chat/index.html', {
        'conversations': _get_conversations(request.user),
    })


@login_required
def private_chat_view(request, other_user_id):
    """Private 1-to-1 chat with another user."""
    other_user = get_object_or_404(User, pk=other_user_id)

    # Mark incoming messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)

    messages = (
        Message.objects
        .filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        )
        .order_by('sent_at')
    )

    uid1, uid2 = sorted([request.user.pk, other_user.pk])
    room_name = f"{uid1}_{uid2}"

    return render(request, 'chat/private.html', {
        'other_user':    other_user,
        'messages':      messages,
        'conversations': _get_conversations(request.user),
        'room_name':     room_name,
    })
