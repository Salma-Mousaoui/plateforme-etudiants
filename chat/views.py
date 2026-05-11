from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import ChatGroup, Message

User = get_user_model()


def get_conversations(user):
    all_messages = (
        Message.objects.filter(
            Q(sender=user) | Q(receiver=user),
            group__isnull=True,
        )
        .select_related("sender", "receiver")
        .order_by("-sent_at")
    )

    seen = set()
    conversations = []
    for msg in all_messages:
        other = msg.receiver if msg.sender == user else msg.sender
        if other and other.id not in seen:
            seen.add(other.id)
            unread = Message.objects.filter(
                sender=other,
                receiver=user,
                is_read=False,
            ).count()
            conversations.append({
                "other_user": other,
                "last_message": msg.content,
                "last_time": msg.sent_at,
                "unread_count": unread,
            })
    return conversations


@login_required
def ChatListView(request):
    conversations = get_conversations(request.user)
    return render(request, "chat/liste_chats.html", {"conversations": conversations})


@login_required
def PrivateChatView(request, other_user_id):
    user = request.user
    other_user = get_object_or_404(User, pk=other_user_id)

    if other_user == user:
        messages.error(request, "You cannot chat with yourself.")
        return redirect("chat-list")

    if request.method == "POST":
        content = request.POST.get("content", "")
        attachment = request.FILES.get("attachment", None)
        if content or attachment:
            Message.objects.create(
                sender=user,
                receiver=other_user,
                content=content,
                attachment=attachment,
            )
        return redirect("private-chat", other_user_id=other_user.id)

    Message.objects.filter(
        sender=other_user, receiver=user, is_read=False
    ).update(is_read=True)

    messages_historique = list(
        Message.objects.filter(
            Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
        ).order_by("sent_at")
    )[-50:]

    return render(request, "chat/chat_prive.html", {
        "other_user": other_user,
        "messages_historique": messages_historique,
        "conversations": get_conversations(user),
    })


@login_required
def GroupChatView(request, group_id):
    user = request.user
    group = get_object_or_404(ChatGroup, pk=group_id)
    if not group.members.filter(pk=user.pk).exists():
        group.members.add(user)
    messages_list = list(
        Message.objects.filter(group=group).order_by("sent_at")
    )[-50:]
    return render(request, "chat/chat_groupe.html", {
        "group": group,
        "messages": messages_list,
    })
