from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .models import ChatGroup, Message

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB


class ChatImageUploadView(LoginRequiredMixin, View):
    """
    Accepts a multipart POST with an image file.
    Saves it via the configured storage backend (Supabase S3 in production)
    and returns the public URL as JSON.

    The caller (browser) is responsible for then sending that URL over the
    WebSocket so Redis only ever carries a short string, never binary data.
    """
    raise_exception = True  # return 403 for unauthenticated AJAX, not a redirect

    def post(self, request, *args, **kwargs):
        image = request.FILES.get("image")

        if not image:
            return JsonResponse(
                {"success": False, "error": "No image provided."}, status=400
            )

        if image.content_type not in ALLOWED_IMAGE_TYPES:
            return JsonResponse(
                {"success": False, "error": "Only JPEG, PNG, GIF and WebP are accepted."},
                status=400,
            )

        if image.size > MAX_IMAGE_BYTES:
            return JsonResponse(
                {"success": False, "error": "Image exceeds the 5 MB limit."},
                status=400,
            )

        other_user_id = request.POST.get("other_user_id")
        receiver = None
        if other_user_id:
            try:
                receiver = get_object_or_404(
                    get_user_model(), pk=int(other_user_id)
                )
            except (ValueError, TypeError):
                return JsonResponse(
                    {"success": False, "error": "Invalid other_user_id."}, status=400
                )

        msg = Message(sender=request.user, content="", receiver=receiver)
        msg.attachment = image
        msg.save()

        return JsonResponse({"success": True, "url": msg.attachment.url})

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


def get_groups_context(user):
    """Return groups data for the sidebar: all groups + set of group IDs the user belongs to."""
    return {
        "available_groups": ChatGroup.objects.all().order_by("city", "name"),
        "my_group_ids": set(
            ChatGroup.objects.filter(members=user).values_list("id", flat=True)
        ),
    }


@login_required
def ChatListView(request):
    ctx = {"conversations": get_conversations(request.user)}
    ctx.update(get_groups_context(request.user))
    return render(request, "chat/liste_chats.html", ctx)


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

    ctx = {
        "other_user": other_user,
        "messages_historique": messages_historique,
        "conversations": get_conversations(user),
    }
    ctx.update(get_groups_context(user))
    return render(request, "chat/chat_prive.html", ctx)


@login_required
def GroupChatView(request, group_id):
    user = request.user
    group = get_object_or_404(ChatGroup, pk=group_id)
    if not group.members.filter(pk=user.pk).exists():
        group.members.add(user)
    messages_list = list(
        Message.objects.filter(group=group)
        .select_related("sender")
        .order_by("sent_at")
    )[-50:]
    ctx = {
        "group": group,
        "messages": messages_list,
        "conversations": get_conversations(user),
    }
    ctx.update(get_groups_context(user))
    return render(request, "chat/chat_groupe.html", ctx)
