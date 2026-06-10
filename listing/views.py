# listing/views.py

from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Room, Unit
from .form import RoomForm, UnitForm



# ────────────── HOME（假角色切換用）──────────────
def home(request):
    """
    首頁 + 假角色切換：
    - /                -> 一般使用者（租客）：is_owner = False
    - /?role=owner     -> 房東模式：is_owner = True
    """
    is_owner = request.GET.get('role') == 'owner'
    context = {
        'is_owner': is_owner,
    }
    return render(request, 'home.html', context)


# ────────────── CHOOSE PAGE ──────────────
def choose_view(request):
    """
    使用者選擇要看 Room 還是 Unit 的頁面
    URL: /listing/choose/
    """
    return render(request, 'choose.html')


# ────────────── ROOM LIST ──────────────
def room_list(request):
    """
    房間列表頁（給租客看的列表）
    URL: /listing/rooms/
    支援簡單搜尋功能（title/location/size）
    """
    query = request.GET.get('q', '').strip()
    rooms = Room.objects.all().order_by('-created_at')

    if query:
        rooms = rooms.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(size__icontains=query)
        )

    context = {
        'rooms': rooms,
        'query': query,
    }
    return render(request, 'room.html', context)


# ────────────── UNIT LIST ──────────────
def unit_list(request):
    """
    整套房（Unit）列表頁（給租客看的列表）
    URL: /listing/units/
    支援簡單搜尋功能（title/location/size/bedrooms/bathrooms）
    """
    query = request.GET.get('q', '').strip()
    units = Unit.objects.all().order_by('-created_at')

    if query:
        units = units.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(size__icontains=query) |
            Q(bedrooms__icontains=query) |
            Q(bathrooms__icontains=query)
        )

    context = {
        'units': units,
        'query': query,
    }
    return render(request, 'unit.html', context)


# ────────────── OWNER DASHBOARD ──────────────
def owner_dashboard(request):
    """
    房東後台總覽頁（Demo 版）
    目前：顯示所有 Room / Unit，不過濾 owner，
    讓你不用登入也不會爆 AnonymousUser 的錯。
    URL: /listing/owner/
    """
    rooms = Room.objects.all().order_by('-created_at')
    units = Unit.objects.all().order_by('-created_at')

    context = {
        'rooms': rooms,
        'units': units,
    }
    return render(request, 'owner.html', context)


# ────────────── OWNER: CREATE ROOM ──────────────
def room_create(request):
    """
    房東新增 Room 的表單頁
    URL: /listing/owner/rooms/new/
    """
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)

            if request.user.is_authenticated:
                room.owner = request.user
            else:
                default_owner = User.objects.first()
                if default_owner is None:
                    raise ValueError(
                        "No User found in database. Please create at least one User."
                    )
                room.owner = default_owner

            room.save()
            return redirect('owner_dashboard')
    else:
        form = RoomForm()

    # 💡 只有這裡改掉：把原本的 'room_form.html' 改成你的真實檔名 'room_create.html'
    return render(request, 'room_create.html', {'form': form})

def unit_create(request):
    """
    房東新增 Unit 的表單頁
    URL: /listing/owner/units/new/
    與 room_create 類似，未登入時會自動指派第一個 User 為 owner。
    """
    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.save(commit=False)

            if request.user.is_authenticated:
                unit.owner = request.user
            else:
                default_owner = User.objects.first()
                if default_owner is None:
                    raise ValueError("No User found in database. Please create at least one User.")
                unit.owner = default_owner

            unit.save()
            return redirect('owner_dashboard')
    else:
        form = UnitForm()

    return render(request, 'unit_form.html', {'form': form})

def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST, request.FILES)
        if form.is_valid():
            unit = form.save(commit=False)

            if request.user.is_authenticated:
                unit.owner = request.user
            else:
                from django.contrib.auth.models import User
                default_owner = User.objects.first()
                if default_owner is None:
                    raise ValueError("No User found in database. Please create at least one User.")
                unit.owner = default_owner

            unit.save()
            return redirect('owner_dashboard')
    else:
        form = UnitForm()

    return render(request, 'unit_form.html', {'form': form})
