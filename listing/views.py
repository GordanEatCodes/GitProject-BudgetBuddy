# listing/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from users.models import UserProfile
from .models import Room, Unit
from .form import RoomForm, UnitForm


# ────────────── Helper: check if user is owner ──────────────
def user_is_owner(user):
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'owner'
    except UserProfile.DoesNotExist:
        return False


# ────────────── HOME ──────────────
def home(request):
    """
    首頁：依照 UserProfile.role 判斷 is_owner
    - 未登入 or 沒有 profile/role -> is_owner = False
    - role == 'owner' -> is_owner = True
    """
    is_owner = False

    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            is_owner = (profile.role == 'owner')
        except UserProfile.DoesNotExist:
            is_owner = False

    return render(request, 'home.html', {'is_owner': is_owner})


# ────────────── CHOOSE PAGE ──────────────
@login_required
def choose_view(request):
    """
    使用者（租客）選擇要看 Room 還是 Unit 的頁面
    URL: /listing/choose/
    """
    return render(request, 'choose.html')


# ────────────── ROOM LIST ──────────────
@login_required
def room_list(request):
    """
    房間列表頁（給租客看的列表）
    URL: /listing/rooms/
    支援搜尋 + 篩選（依你之前的欄位）
    """
    query = request.GET.get('q', '').strip()

    state = request.GET.get('state', '').strip()
    unit_type = request.GET.get('unit_type', '').strip()
    floor_level = request.GET.get('floor_level', '').strip()
    bathroom_type = request.GET.get('bathroom_type', '').strip()

    rooms = Room.objects.all().order_by('-created_at')

    if query:
        rooms = rooms.filter(
            Q(title__icontains=query) |
            Q(location_detail__icontains=query) |
            Q(size__icontains=query)
        )

    if state:
        rooms = rooms.filter(state=state)

    if unit_type:
        rooms = rooms.filter(unit_type=unit_type)

    if floor_level:
        rooms = rooms.filter(floor_level=floor_level)

    if bathroom_type:
        rooms = rooms.filter(bathroom_type=bathroom_type)

    context = {
        'rooms': rooms,
        'query': query,
        'state': state,
        'unit_type': unit_type,
        'floor_level': floor_level,
        'bathroom_type': bathroom_type,
    }
    return render(request, 'room.html', context)


# ────────────── UNIT LIST ──────────────
@login_required
def unit_list(request):
    """
    整套房（Unit）列表頁（給租客看的列表）
    URL: /listing/units/
    支援搜尋 + 基本篩選
    """
    query = request.GET.get('q', '').strip()

    state = request.GET.get('state', '').strip()
    unit_type = request.GET.get('unit_type', '').strip()
    floor_level = request.GET.get('floor_level', '').strip()
    bedrooms = request.GET.get('bedrooms', '').strip()
    bathrooms = request.GET.get('bathrooms', '').strip()

    units = Unit.objects.all().order_by('-created_at')

    if query:
        units = units.filter(
            Q(title__icontains=query) |
            Q(location_detail__icontains=query) |
            Q(size__icontains=query)
        )

    if state:
        units = units.filter(state=state)

    if unit_type:
        units = units.filter(unit_type=unit_type)

    if floor_level:
        units = units.filter(floor_level=floor_level)

    if bedrooms:
        units = units.filter(bedrooms=bedrooms)

    if bathrooms:
        units = units.filter(bathrooms=bathrooms)

    context = {
        'units': units,
        'query': query,
        'state': state,
        'unit_type': unit_type,
        'floor_level': floor_level,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
    }
    return render(request, 'unit.html', context)


# ────────────── OWNER DASHBOARD ──────────────
@login_required
def owner_dashboard(request):
    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to access this page.")

    rooms = Room.objects.filter(owner=request.user).order_by('-created_at')
    units = Unit.objects.filter(owner=request.user).order_by('-created_at')

    return render(request, 'owner.html', {'rooms': rooms, 'units': units})


# ────────────── OWNER: CREATE ROOM ──────────────
@login_required
def room_create(request):
    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to create room listings.")

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = request.user
            room.save()
            return redirect('owner_dashboard')
    else:
        form = RoomForm()
    return render(request, 'room_form.html', {'form': form})


# ────────────── OWNER: CREATE UNIT ──────────────
@login_required
def unit_create(request):
    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to create unit listings.")

    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.owner = request.user
            unit.save()
            return redirect('owner_dashboard')
    else:
        form = UnitForm()
    return render(request, 'unit_form.html', {'form': form})

@login_required
def room_detail(request, pk):
    """
    單一 Room 詳情頁
    URL: /listing/rooms/<pk>/
    """
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'room_detail.html', {'room': room})