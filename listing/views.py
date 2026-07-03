# listing/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Case, When, IntegerField, Value
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from users.models import UserProfile
from .models import Room, Unit, RoomRequest, UnitRequest, RoomImage, UnitImage
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
    支援搜尋 + 篩選 + 相關度排序 + 分類結果
    """
    query = request.GET.get('q', '').strip()
    state = request.GET.get('state', '').strip()
    city = request.GET.get('city', '').strip()
    unit_type = request.GET.get('unit_type', '').strip()
    floor_level = request.GET.get('floor_level', '').strip()
    bathroom_type = request.GET.get('bathroom_type', '').strip()

    rooms = Room.objects.filter(available=True)

    filter_applied = bool(state or city or unit_type or floor_level or bathroom_type)

    # 基本篩選（非位置類）
    if unit_type:
        rooms = rooms.filter(unit_type=unit_type)
    if floor_level:
        rooms = rooms.filter(floor_level=floor_level)
    if bathroom_type:
        rooms = rooms.filter(bathroom_type=bathroom_type)

    # Characteristic checkbox 篩選
    checkbox_fields = [
        'near_mrt', 'near_lrt', 'near_ktm', 'near_bus_stop',
        'security_24h', 'swimming_pool', 'gym_room', 'covered_carpark',
        'oku_friendly', 'multi_purpose_hall', 'playground', 'has_surau',
        'near_mini_market', 'co_living', 'extra_parking',
        'has_aircond', 'has_washing_machine', 'has_wifi', 'cooking_allowed',
        'has_tv', 'shared_bathroom', 'private_bathroom', 'has_shower',
        'pet_allowed', 'smoking_allowed',
        'prefer_zero_deposit', 'prefer_move_in_immediately',
        'prefer_pet_allowed', 'prefer_muslim_friendly', 'prefer_smoking_allowed',
    ]
    for field in checkbox_fields:
        if request.GET.get(field) == 'on':
            rooms = rooms.filter(**{field: True})

    # keyword 搜尋（在拆分 exact/other 之前先過濾）
    if query:
        rooms = rooms.filter(
            Q(title__icontains=query) |
            Q(location_detail__icontains=query) |
            Q(size__icontains=query)
        )

    # 排序
    rooms = rooms.order_by('-created_at')

    # ─── 分成 exact_match 和 other_results ───
    # 優先順序：city > state
    if city:
        # 精確：同 city；其他：同 state 但不同 city + 其他 state
        exact_match = rooms.filter(city=city)
        other_results = rooms.exclude(city=city)
    elif state:
        # 精確：同 state；其他：其他 state
        exact_match = rooms.filter(state=state)
        other_results = rooms.exclude(state=state)
    else:
        exact_match = rooms
        other_results = rooms.none()

    context = {
        'rooms': exact_match,
        'other_results': other_results,
        'query': query,
        'state': state,
        'city': city,
        'unit_type': unit_type,
        'floor_level': floor_level,
        'bathroom_type': bathroom_type,
        'has_filters': filter_applied,
    }
    return render(request, 'room.html', context)



# ────────────── UNIT LIST ──────────────
@login_required
def unit_list(request):
    """
    整套房（Unit）列表頁
    URL: /listing/units/
    支援搜尋 + 篩選 + 分類結果
    """
    query = request.GET.get('q', '').strip()
    state = request.GET.get('state', '').strip()
    city = request.GET.get('city', '').strip()
    unit_type = request.GET.get('unit_type', '').strip()
    floor_level = request.GET.get('floor_level', '').strip()
    bedrooms = request.GET.get('bedrooms', '').strip()
    bathrooms = request.GET.get('bathrooms', '').strip()

    units = Unit.objects.filter(available=True)

    filter_applied = bool(state or city or unit_type or floor_level or bedrooms or bathrooms)

    # 基本篩選（非位置類）
    if unit_type:
        units = units.filter(unit_type=unit_type)
    if floor_level:
        units = units.filter(floor_level=floor_level)
    if bedrooms:
        units = units.filter(bedrooms=bedrooms)
    if bathrooms:
        units = units.filter(bathrooms=bathrooms)

    # Characteristic checkbox 篩選
    checkbox_fields = [
        'near_mrt', 'near_lrt', 'near_ktm', 'near_bus_stop',
        'security_24h', 'swimming_pool', 'gym_room', 'covered_carpark',
        'oku_friendly', 'multi_purpose_hall', 'playground', 'has_surau',
        'near_mini_market', 'co_living', 'extra_parking',
        'has_aircond', 'has_washing_machine', 'has_wifi', 'cooking_allowed',
        'has_tv', 'shared_bathroom', 'private_bathroom', 'has_shower',
        'pet_allowed', 'smoking_allowed',
    ]
    for field in checkbox_fields:
        if request.GET.get(field) == 'on':
            # 只篩 Unit 有的欄位（避免報錯）
            if field in [f.name for f in Unit._meta.get_fields()]:
                units = units.filter(**{field: True})

    # keyword 搜尋
    if query:
        units = units.filter(
            Q(title__icontains=query) |
            Q(location_detail__icontains=query) |
            Q(size__icontains=query)
        )

    # 排序
    units = units.order_by('-created_at')

    # ─── 分成 exact_match 和 other_results ───
    if city:
        exact_match = units.filter(city=city)
        other_results = units.exclude(city=city)
    elif state:
        exact_match = units.filter(state=state)
        other_results = units.exclude(state=state)
    else:
        exact_match = units
        other_results = units.none()

    context = {
        'units': exact_match,
        'other_results': other_results,
        'query': query,
        'state': state,
        'city': city,
        'unit_type': unit_type,
        'floor_level': floor_level,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'has_filters': filter_applied,
    }
    return render(request, 'unit.html', context)


# ────────────── OWNER DASHBOARD ──────────────
@login_required
def owner_dashboard(request):
    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to access this page.")

    # 這個 owner 自己的房源
    rooms = Room.objects.filter(owner=request.user).order_by('-created_at')
    units = Unit.objects.filter(owner=request.user).order_by('-created_at')

    # 這個 owner 房間的所有 requests
    room_requests = RoomRequest.objects.filter(
        room__owner=request.user
    ).select_related('room', 'tenant').order_by('-created_at')

    # 這個 owner 單位的所有 requests
    unit_requests = UnitRequest.objects.filter(
        unit__owner=request.user
    ).select_related('unit', 'tenant').order_by('-created_at')

    # Debug 輸出，看實際抓到多少筆
    print("DEBUG room_requests count:", room_requests.count())
    print("DEBUG unit_requests count:", unit_requests.count())

    context = {
        'rooms': rooms,
        'units': units,
        'room_requests': room_requests,
        'unit_requests': unit_requests,
    }
    return render(request, 'owner.html', context)


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

            for img in request.FILES.getlist('extra_images'):
                RoomImage.objects.create(room=room, image=img)

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

            # 處理多張圖片
            for img in request.FILES.getlist('extra_images'):
                UnitImage.objects.create(unit=unit, image=img)

            return redirect('owner_dashboard')
    else:
        form = UnitForm()
    return render(request, 'unit_form.html', {'form': form})



@login_required
def room_detail(request, pk):
    """
    單一 Room 詳情頁 + 處理租房請求
    URL: /listing/rooms/<pk>/
    """
    room = get_object_or_404(Room, pk=pk)

    # 找出目前使用者對這個 room 的最新 request（如果有）
    current_request = None
    if request.user.is_authenticated:
        current_request = RoomRequest.objects.filter(
            room=room,
            tenant=request.user
        ).order_by('-created_at').first()

    if request.method == 'POST':
        # 如果已經有 pending 或 accepted，就不要再重複送
        if current_request and current_request.status in ['pending', 'accepted']:
            return redirect('room_detail', pk=room.pk)

        # 建立一筆新的 pending request（不需要 message）
        RoomRequest.objects.create(
            room=room,
            tenant=request.user,
            status='pending'
        )
        return redirect('room_detail', pk=room.pk)

    context = {
        'room': room,
        'current_request': current_request,
    }
    return render(request, 'room_detail.html', context)



@login_required
def unit_detail(request, pk):
    """
    單一 Unit 詳情頁 + 處理租房請求
    URL: /listing/units/<pk>/
    """
    unit = get_object_or_404(Unit, pk=pk)

    # 找出目前使用者對這個 unit 的最新 request（如果有）
    current_request = None
    if request.user.is_authenticated:
        current_request = UnitRequest.objects.filter(
            unit=unit,
            tenant=request.user
        ).order_by('-created_at').first()

    if request.method == 'POST':
        # 如果已經有 pending 或 accepted，就不要再重複送
        if current_request and current_request.status in ['pending', 'accepted']:
            return redirect('unit_detail', pk=unit.pk)

        UnitRequest.objects.create(
            unit=unit,
            tenant=request.user,
            status='pending'
        )
        return redirect('unit_detail', pk=unit.pk)

    context = {
        'unit': unit,
        'current_request': current_request,
    }
    return render(request, 'unit_detail.html', context)


@login_required
def room_request_action(request, request_id, action):
    """
    房東對 RoomRequest 做 accept / reject
    URL: /listing/owner/requests/<id>/<action>/
    """
    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to perform this action.")

    req = get_object_or_404(RoomRequest, pk=request_id, room__owner=request.user)

    if request.method == 'POST':
        if action not in ['accept', 'reject']:
            return HttpResponseForbidden("Invalid action.")

        if action == 'accept':
            req.status = 'accepted'
        elif action == 'reject':
            req.status = 'rejected'

        req.decision_at = timezone.now()
        req.save()
        return redirect('owner_dashboard')

    return HttpResponseForbidden("Invalid request method.")

@login_required
def unit_request_action(request, request_id, action):
    """
    房東對 UnitRequest 做 accept / reject
    URL: /listing/owner/unit-requests/<id>/<action>/
    """
    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to perform this action.")

    req = get_object_or_404(UnitRequest, pk=request_id, unit__owner=request.user)

    if request.method == 'POST':
        if action not in ['accept', 'reject']:
            return HttpResponseForbidden("Invalid action.")

        if action == 'accept':
            req.status = 'accepted'
        elif action == 'reject':
            req.status = 'rejected'

        req.decision_at = timezone.now()
        req.save()
        return redirect('owner_dashboard')

    return HttpResponseForbidden("Invalid request method.")



@login_required
def my_room_requests(request):
    """
    租客自己的租房請求列表（Rooms + Units）
    URL: /listing/my-requests/rooms/
    """
    room_requests_qs = RoomRequest.objects.filter(
        tenant=request.user
    ).select_related('room').order_by('-created_at')

    unit_requests_qs = UnitRequest.objects.filter(
        tenant=request.user
    ).select_related('unit').order_by('-created_at')

    context = {
        'room_requests': room_requests_qs,
        'unit_requests': unit_requests_qs,
    }
    return render(request, 'my_room_requests.html', context)

# ────────────── OWNER: EDIT ROOM ──────────────
@login_required
def room_edit(request, pk):
    # 只能編輯自己的房源
    room = get_object_or_404(Room, pk=pk, owner=request.user)

    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to edit room listings.")

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()

            # 如果有上傳新的額外照片，繼續加到 RoomImage
            for img in request.FILES.getlist('extra_images'):
                RoomImage.objects.create(room=room, image=img)

            return redirect('owner_dashboard')
    else:
        form = RoomForm(instance=room)

    return render(request, 'room_form.html', {'form': form, 'edit_mode': True, 'room': room})


# ────────────── OWNER: TOGGLE ROOM AVAILABLE ──────────────
@login_required
def room_toggle_available(request, pk):
    """
    快速上架 / 下架（切換 available）
    """
    room = get_object_or_404(Room, pk=pk, owner=request.user)

    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to perform this action.")

    if request.method == 'POST':
        room.available = not room.available
        room.save()

    return redirect('owner_dashboard')

# ────────────── OWNER: EDIT UNIT ──────────────
@login_required
def unit_edit(request, pk):
    """
    房東編輯自己的 Unit
    URL: /listing/owner/units/<pk>/edit/
    """
    unit = get_object_or_404(Unit, pk=pk, owner=request.user)

    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to edit unit listings.")

    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES, instance=unit)
        if form.is_valid():
            form.save()

            # 如果有上傳新的額外照片
            for img in request.FILES.getlist('extra_images'):
                UnitImage.objects.create(unit=unit, image=img)

            return redirect('owner_dashboard')
    else:
        form = UnitForm(instance=unit)

    return render(request, 'unit_form.html', {'form': form, 'edit_mode': True, 'unit': unit})

# ────────────── OWNER: TOGGLE UNIT AVAILABLE ──────────────
@login_required
def unit_toggle_available(request, pk):
    """
    房東快速上架 / 下架 Unit（切換 available）
    URL: /listing/owner/units/<pk>/toggle/
    """
    unit = get_object_or_404(Unit, pk=pk, owner=request.user)

    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to perform this action.")

    if request.method == 'POST':
        unit.available = not unit.available
        unit.save()

    return redirect('owner_dashboard')

@login_required
def room_delete(request, pk):
    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to delete room listings.")

    room = get_object_or_404(Room, pk=pk, owner=request.user)

    if request.method == 'POST':
        room.delete()
        return redirect('owner_dashboard')

    return HttpResponseForbidden("Invalid request method.")


@login_required
def unit_delete(request, pk):
    if not user_is_owner(request.user):
        return HttpResponseForbidden("You are not allowed to delete unit listings.")

    unit = get_object_or_404(Unit, pk=pk, owner=request.user)

    if request.method == 'POST':
        unit.delete()
        return redirect('owner_dashboard')

    return HttpResponseForbidden("Invalid request method.")

@login_required
def my_room_request_delete(request, request_id):
    req = get_object_or_404(RoomRequest, pk=request_id, tenant=request.user)

    if request.method == 'POST':
        req.delete()
        return redirect('my_room_requests')

    return HttpResponseForbidden("Invalid request method.")


@login_required
def my_unit_request_delete(request, request_id):
    req = get_object_or_404(UnitRequest, pk=request_id, tenant=request.user)

    if request.method == 'POST':
        req.delete()
        return redirect('my_room_requests')

    return HttpResponseForbidden("Invalid request method.")
