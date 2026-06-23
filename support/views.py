import uuid
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone

from .models import ChatSession, ChatMessage

GUEST_COOKIE_NAME = 'bb_chat_guest_id'
GUEST_COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 year


def is_agent(user):
    return user.is_authenticated and user.is_staff  # Simple check, can be extended to use groups/permissions


def get_or_create_session(request):
    if request.user.is_authenticated:
        session = ChatSession.objects.filter(user=request.user, status='open').order_by('-created_at').first()
        if session:
            return session, None
        return ChatSession.objects.create(user=request.user), None

    guest_id = request.COOKIES.get(GUEST_COOKIE_NAME)
    session = None
    if guest_id:
        session = ChatSession.objects.filter(guest_id=guest_id, status='open').order_by('-created_at').first()
    new_cookie = None
    if not session:
        guest_id = str(uuid.uuid4())
        session = ChatSession.objects.create(guest_id=guest_id)
        new_cookie = guest_id
    return session, new_cookie


def contact_us(request):
    session, new_guest_id = get_or_create_session(request)
    response = render(request, 'support/contact_us.html', {
        'chat_session': session,
        'chat_history': session.messages.all(),
    })
    if new_guest_id:
        response.set_cookie(GUEST_COOKIE_NAME, new_guest_id, max_age=GUEST_COOKIE_MAX_AGE)
    return response

def contact_dash(request):
    if not request.user.is_authenticated:
        return redirect('support:contact_us')

    session, new_guest_id = get_or_create_session(request)
    response = render(request, 'support/contact_us_dash.html', {  
        'chat_session': session,
        'chat_history': session.messages.all(),
    })
    if new_guest_id:
        response.set_cookie(GUEST_COOKIE_NAME, new_guest_id, max_age=GUEST_COOKIE_MAX_AGE)
    return response

def can_access_session(request, session):
    if request.user.is_authenticated:
        if is_agent(request.user):
            return True
        return session.user_id == request.user.id
    guest_id = request.COOKIES.get(GUEST_COOKIE_NAME)
    return bool(guest_id) and session.guest_id == guest_id


@require_POST
def send_message(request, session_id):
    session = get_object_or_404(ChatSession, pk=session_id)
    if not can_access_session(request, session):
        return HttpResponseForbidden()

    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Empty message'}, status=400)

    sender_type = ChatMessage.SENDER_AGENT if is_agent(request.user) else ChatMessage.SENDER_VISITOR
    message = ChatMessage.objects.create(
        session=session,
        sender_type=sender_type,
        sender=request.user if request.user.is_authenticated else None,
        content=content,
    )
    session.last_message_at = timezone.now()
    session.save(update_fields=['last_message_at'])

    return JsonResponse({
        'id': message.id,
        'sender_type': message.sender_type,
        'content': message.content,
        'created_at': message.created_at.strftime('%H:%M'),
    })


@require_GET
def poll_messages(request, session_id):
    session = get_object_or_404(ChatSession, pk=session_id)
    if not can_access_session(request, session):
        return HttpResponseForbidden()

    after_id = request.GET.get('after', 0)
    messages = session.messages.filter(id__gt=after_id)
    data = [{
        'id': m.id, 'sender_type': m.sender_type,
        'content': m.content, 'created_at': m.created_at.strftime('%H:%M'),
    } for m in messages]
    return JsonResponse({'messages': data, 'status': session.status})


@login_required
def agent_inbox(request):
    if not is_agent(request.user):
        return HttpResponseForbidden("You are not a support agent.")
    return render(request, 'support/agent_inbox.html', {
        'unassigned': ChatSession.objects.filter(status='open', assigned_agent__isnull=True),
        'my_chats': ChatSession.objects.filter(status='open', assigned_agent=request.user),
    })


@login_required
def agent_claim(request, session_id):
    if not is_agent(request.user):
        return HttpResponseForbidden()
    session = get_object_or_404(ChatSession, pk=session_id, assigned_agent__isnull=True)
    session.assigned_agent = request.user
    session.save(update_fields=['assigned_agent'])
    return redirect('support:agent_chat', session_id=session.id)


@login_required
def agent_chat(request, session_id):
    if not is_agent(request.user):
        return HttpResponseForbidden()
    session = get_object_or_404(ChatSession, pk=session_id)
    return render(request, 'support/agent_chat.html', {
        'chat_session': session,
        'chat_history': session.messages.all(),
    })


@login_required
def agent_close_chat(request, session_id):
    if not is_agent(request.user):
        return HttpResponseForbidden()
    session = get_object_or_404(ChatSession, pk=session_id, assigned_agent=request.user)
    session.status = ChatSession.STATUS_CLOSED
    session.save(update_fields=['status'])
    return redirect('support:agent_inbox')