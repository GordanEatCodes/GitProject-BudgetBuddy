from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import RoommatePost, RoommateApplication, RoommateMessage, RoommateFavourite
from users.models import UserProfile

import string


def normalize_text(text):
    if not text:
        return ""

    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = " ".join(text.split())

    return text


def to_float(value):
    try:
        return float(value) if value else None
    except ValueError:
        return None


def to_int(value, default=1):
    try:
        number = int(value)
        return number if number > 0 else default
    except (TypeError, ValueError):
        return default


def get_user_profile_preferences(user):
    """
    Get preferences from users.UserProfile and convert them
    into RoommatePost field values.

    UserProfile:
    - state -> location
    - phone_number -> contact
    - cleanliness integer -> cleanliness choice
    - sleep_schedule -> sleep_schedule choice
    - study_habits / noise_tolerance -> study_preference choice
    """

    preferences = {
        'location': '',
        'contact': '',
        'cleanliness': 'any',
        'sleep_schedule': 'any',
        'study_preference': 'any',
        'smoking': 'any',
        'pets': 'any',
    }

    if not user.is_authenticated:
        return preferences

    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        return preferences

    # Auto-fill location and contact from user profile
    preferences['location'] = profile.state or ''
    preferences['contact'] = profile.phone_number or ''

    # Convert cleanliness score into RoommatePost choices
    cleanliness_score = profile.cleanliness or 3

    if cleanliness_score >= 4:
        preferences['cleanliness'] = 'very_clean'
    elif cleanliness_score == 3:
        preferences['cleanliness'] = 'normal'
    elif cleanliness_score <= 2:
        preferences['cleanliness'] = 'messy'

    # Convert sleep schedule into RoommatePost choices
    sleep_schedule = (profile.sleep_schedule or '').lower().replace(' ', '_').replace('-', '_')

    if 'early' in sleep_schedule:
        preferences['sleep_schedule'] = 'early_sleep'
    elif 'late' in sleep_schedule:
        preferences['sleep_schedule'] = 'late_sleep'
    elif 'flex' in sleep_schedule:
        preferences['sleep_schedule'] = 'flexible'
    elif sleep_schedule in ['early_sleep', 'late_sleep', 'flexible']:
        preferences['sleep_schedule'] = sleep_schedule

    # Convert study habits into RoommatePost choices
    study_habits = (profile.study_habits or '').lower().replace(' ', '_').replace('-', '_')

    if 'quiet' in study_habits:
        preferences['study_preference'] = 'quiet'
    elif 'social' in study_habits or 'group' in study_habits:
        preferences['study_preference'] = 'social'
    elif 'normal' in study_habits:
        preferences['study_preference'] = 'normal'
    else:
        # If study_habits is empty, use noise_tolerance as backup
        noise_score = profile.noise_tolerance or 3

        if noise_score <= 2:
            preferences['study_preference'] = 'quiet'
        elif noise_score >= 4:
            preferences['study_preference'] = 'social'
        else:
            preferences['study_preference'] = 'normal'

    return preferences


def update_roommate_post_status(post):
    accepted_count = post.applications.filter(status='accepted').count()

    if post.post_status != 'closed':
        if accepted_count >= post.needed_roommates:
            post.post_status = 'full'
        else:
            post.post_status = 'open'

        post.save()


@login_required(login_url='/login/')
def add_roommate(request):
    profile_preferences = get_user_profile_preferences(request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        budget = request.POST.get('budget')
        contact = request.POST.get('contact')

        RoommatePost.objects.create(
            title=title,
            description=description,
            location=location,
            budget=float(budget) if budget else 0,
            contact=contact,

            unit_name=request.POST.get('unit_name', ''),
            total_rent=to_float(request.POST.get('total_rent')),
            total_people=to_int(request.POST.get('total_people'), 1),
            needed_roommates=to_int(request.POST.get('needed_roommates'), 1),
            post_status='open',

            cleanliness=request.POST.get('cleanliness', profile_preferences['cleanliness']),
            sleep_schedule=request.POST.get('sleep_schedule', profile_preferences['sleep_schedule']),
            study_preference=request.POST.get('study_preference', profile_preferences['study_preference']),
            smoking=request.POST.get('smoking', 'any'),
            pets=request.POST.get('pets', 'any'),

            preferred_pet=request.POST.get(
                'preferred_pet',
                ''
            ),

            created_by=request.user,
        )

        messages.success(
           request,
           "Roommate post created successfully!"
        )

        return redirect('roommate_list')

    return render(request, 'roommate/add_roommate.html', {
        'profile_preferences': profile_preferences
    })


def roommate_list(request):
    posts = RoommatePost.objects.all()

    location = request.GET.get('location')
    max_budget = request.GET.get('max_budget')
    sort = request.GET.get('sort')

    if location:
        posts = posts.filter(location__icontains=location)

    if max_budget:
        try:
            posts = posts.filter(budget__lte=float(max_budget))
        except ValueError:
            pass

    if sort == 'oldest':
        posts = posts.order_by('created_at')
    elif sort == 'low_budget':
        posts = posts.order_by('budget')
    elif sort == 'high_budget':
        posts = posts.order_by('-budget')
    else:
        posts = posts.order_by('-created_at')

    saved_post_ids = []

    if request.user.is_authenticated:
        saved_post_ids = list(
            RoommateFavourite.objects.filter(user=request.user)
            .values_list('roommate_post_id', flat=True)
        )

    return render(request, 'roommate/roommate_list.html', {
        'posts': posts,
        'location': location,
        'max_budget': max_budget,
        'sort': sort,
        'saved_post_ids': saved_post_ids,
    })


def roommate_detail(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    is_saved = False

    if request.user.is_authenticated:
        is_saved = RoommateFavourite.objects.filter(
            user=request.user,
            roommate_post=post
        ).exists()

    return render(request, 'roommate/roommate_detail.html', {
        'post': post,
        'is_saved': is_saved,
    })


@login_required(login_url='/login/')
def delete_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    if post.created_by != request.user:
        return redirect('roommate_detail', id=post.id)

    if request.method == 'POST':
        post.delete()

        messages.success(
            request,
            "Roommate post deleted successfully!"
        )

        return redirect('roommate_list')

    return render(
        request,
        'roommate/confirm_delete.html',
        {
            'post': post
        }
    )


@login_required(login_url='/login/')
def edit_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    if post.created_by != request.user:
        return redirect('roommate_detail', id=post.id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')
        post.location = request.POST.get('location')

        budget = request.POST.get('budget')
        if budget:
            post.budget = float(budget)

        post.contact = request.POST.get('contact')

        post.unit_name = request.POST.get('unit_name', '')
        post.total_rent = to_float(request.POST.get('total_rent'))
        post.total_people = to_int(request.POST.get('total_people'), 1)
        post.needed_roommates = to_int(request.POST.get('needed_roommates'), 1)
        post.post_status = request.POST.get('post_status', 'open')

        post.cleanliness = request.POST.get('cleanliness', 'any')
        post.sleep_schedule = request.POST.get('sleep_schedule', 'any')
        post.study_preference = request.POST.get('study_preference', 'any')
        post.smoking = request.POST.get('smoking', 'any')
        post.preferred_pet = request.POST.get(
            'preferred_pet',
            ''
            )

        post.save()

        messages.success(
            request,
            "Roommate post updated successfully!"
        )

        return redirect('roommate_list')

    return render(request, 'roommate/edit_roommate.html', {
        'post': post
    })


def match_roommates(request, id):
    current_user_post = get_object_or_404(RoommatePost, id=id)

    # Only recommend open posts
    all_posts = RoommatePost.objects.exclude(id=id).filter(post_status='open')

    results = []

    stop_words = {
        "i", "am", "is", "are", "the", "and", "or", "a", "an",
        "to", "for", "with", "in", "on", "of", "my", "me",
        "looking", "roommate", "room", "student", "want", "need"
    }

    for post in all_posts:
        score = 0
        reasons = []

        # 1. Location match - max 25
        current_location = normalize_text(current_user_post.location)
        post_location = normalize_text(post.location)

        current_location_no_space = current_location.replace(" ", "")
        post_location_no_space = post_location.replace(" ", "")

        if current_location_no_space == post_location_no_space:
            score += 25
            reasons.append("Same location")
        elif current_location_no_space in post_location_no_space or post_location_no_space in current_location_no_space:
            score += 15
            reasons.append("Similar location")
        else:
            reasons.append("Different location")

        # 2. Budget similarity - max 25
        budget_diff = abs(float(current_user_post.budget) - float(post.budget))

        if budget_diff <= 100:
            score += 25
            reasons.append("Budget difference is within RM100")
        elif budget_diff <= 200:
            score += 18
            reasons.append("Budget difference is within RM200")
        elif budget_diff <= 300:
            score += 10
            reasons.append("Budget difference is within RM300")
        else:
            reasons.append("Budget difference is more than RM300")

        # 3. Lifestyle preference matching - max 35
        lifestyle_fields = [
            ('cleanliness', 'Cleanliness preference'),
            ('sleep_schedule', 'Sleep schedule'),
            ('study_preference', 'Study preference'),
            ('smoking', 'Smoking preference'),
            ('pets', 'Pet preference'),
        ]

        for field_name, label in lifestyle_fields:
            current_value = getattr(current_user_post, field_name, 'any')
            post_value = getattr(post, field_name, 'any')

            if current_value == post_value and current_value != 'any':
                score += 7
                reasons.append(f"{label} matched")
            elif current_value == 'any' or post_value == 'any':
                score += 3
                reasons.append(f"{label} is flexible")
            else:
                reasons.append(f"{label} is different")

        # Pet Details comparison (informational only)
        current_pet_details = normalize_text(current_user_post.preferred_pet)
        post_pet_details = normalize_text(post.preferred_pet)

        if current_pet_details and post_pet_details:

            current_pet_words = set(current_pet_details.split())
            post_pet_words = set(post_pet_details.split())

            common_pets = current_pet_words & post_pet_words

            if common_pets:
                reasons.append(
                    "Similar pet preference: "
                    + ", ".join(sorted(common_pets))
                )
            else:
                reasons.append(
                    "Different pet preference"
                )

        elif current_pet_details or post_pet_details:

            reasons.append(
                "Only one post specifies pet details"
            )

        # 4. Description keyword similarity - max 15
        current_description = normalize_text(current_user_post.description)
        post_description = normalize_text(post.description)

        current_words = set(current_description.split()) - stop_words
        post_words = set(post_description.split()) - stop_words

        current_words = set(current_description.split()) - stop_words
        post_words = set(post_description.split()) - stop_words

        common_words = current_words & post_words
        keyword_score = min(len(common_words) * 3, 15)

        score += keyword_score

        if common_words:
            reasons.append("Similar keywords: " + ", ".join(common_words))
        else:
            reasons.append("No strong keyword similarity")

        match_percentage = min(score, 100)

        if match_percentage >= 80:
            match_label = "Excellent Match"
        elif match_percentage >= 60:
            match_label = "Good Match"
        elif match_percentage >= 40:
            match_label = "Fair Match"
        else:
            match_label = "Low Match"

        results.append({
            'post': post,
            'score': score,
            'match_percentage': match_percentage,
            'match_label': match_label,
            'reasons': reasons
        })

    results.sort(key=lambda x: x['match_percentage'], reverse=True)

    best_match = results[0] if results else None

    return render(request, 'roommate/match.html', {
        'current': current_user_post,
        'best_match': best_match,
        'matches': results
    })


@login_required(login_url='/login/')
def apply_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    if post.created_by is None:
        return redirect('roommate_detail', id=post.id)

    if post.post_status != 'open':
        return redirect('roommate_detail', id=post.id)

    if post.created_by == request.user:
        return redirect('roommate_detail', id=post.id)

    existing_application = RoommateApplication.objects.filter(
        roommate_post=post,
        applicant=request.user
    ).first()

    if existing_application:
        return redirect('application_detail', application_id=existing_application.id)

    if request.method == 'POST':
        message = request.POST.get('message')

        application = RoommateApplication.objects.create(
            roommate_post=post,
            applicant=request.user,
            message=message,
            status='pending'
        )

        if message:
            RoommateMessage.objects.create(
                application=application,
                sender=request.user,
                message=message
            )

    messages.success(
        request,
        "Application submitted successfully!"
    )

    return redirect('my_roommate_applications')

    return render(request, 'roommate/apply_roommate.html', {
        'post': post
    })


@login_required(login_url='/login/')
def applications_received(request):
    applications = RoommateApplication.objects.filter(
        roommate_post__created_by=request.user
    ).order_by('-created_at')

    return render(request, 'roommate/applications_received.html', {
        'applications': applications
    })


@login_required(login_url='/login/')
def my_roommate_applications(request):
    applications = RoommateApplication.objects.filter(
        applicant=request.user
    ).order_by('-created_at')

    return render(request, 'roommate/my_applications.html', {
        'applications': applications
    })


@login_required(login_url='/login/')
def update_application_status(request, application_id, status):
    application = get_object_or_404(RoommateApplication, id=application_id)

    if application.roommate_post.created_by != request.user:
        return redirect('roommate_list')

    if status not in ['pending', 'accepted', 'rejected']:
        return redirect('applications_received')

    if request.method == 'POST':
        application.status = status
        application.save()

        update_roommate_post_status(application.roommate_post)

        if status == "accepted":
            messages.success(
                request,
                "Application accepted successfully!"
             )

        elif status == "rejected":
            messages.success(
                request,
                "Application rejected successfully!"
            )

        else:
            messages.success(
                 request,
                 "Application updated successfully!"
             )

        update_roommate_post_status(application.roommate_post)

    return redirect('applications_received')


@login_required(login_url='/login/')
def cancel_accepted_application(request, application_id):
    application = get_object_or_404(RoommateApplication, id=application_id)

    if application.applicant != request.user:
        return redirect('roommate_list')

    if request.method == 'POST':
        if application.status == 'accepted':
            application.status = 'pending'
            application.save()

            update_roommate_post_status(application.roommate_post)

            messages.success(
                request,
                "Accepted application has been cancelled."
            )

    return redirect('my_roommate_applications')


@login_required(login_url='/login/')
def application_detail(request, application_id):
    application = get_object_or_404(RoommateApplication, id=application_id)

    is_applicant = application.applicant == request.user
    is_coordinator = application.roommate_post.created_by == request.user

    if not is_applicant and not is_coordinator:
        return redirect('roommate_list')

    if request.method == 'POST':
        message = request.POST.get('message')

        if message:
            RoommateMessage.objects.create(
                application=application,
                sender=request.user,
                message=message
            )

        return redirect('application_detail', application_id=application.id)

    chat_messages = application.messages.all()

    return render(request, 'roommate/application_detail.html', {
        'application': application,
        'messages': chat_messages
    })


@login_required(login_url='/login/')
def close_roommate_post(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    if post.created_by != request.user:
        return redirect('roommate_detail', id=post.id)

    if request.method == 'POST':
        post.post_status = 'closed'
        post.save()

        messages.success(
            request,
            "Roommate post closed successfully!"
        )

    return redirect('roommate_detail', id=post.id)


@login_required(login_url='/login/')
def reopen_roommate_post(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    if post.created_by != request.user:
        return redirect('roommate_detail', id=post.id)

    if request.method == 'POST':
        accepted_count = post.applications.filter(status='accepted').count()

        if accepted_count >= post.needed_roommates:
            post.post_status = 'full'
        else:
            post.post_status = 'open'

        post.save()
        messages.success(
            request,
             "Roommate post reopened successfully!"
        )

    return redirect('roommate_detail', id=post.id)


@login_required(login_url='/login/')
def roommate_dashboard(request):
    user_posts = RoommatePost.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    received_applications = RoommateApplication.objects.filter(
        roommate_post__created_by=request.user
    ).order_by('-created_at')[:5]

    my_applications = RoommateApplication.objects.filter(
        applicant=request.user
    ).order_by('-created_at')[:5]

    saved_posts = RoommateFavourite.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    total_posts = user_posts.count()

    open_posts_count = user_posts.filter(
        post_status='open'
    ).count()

    pending_received_count = RoommateApplication.objects.filter(
        roommate_post__created_by=request.user,
        status='pending'
    ).count()

    pending_my_applications_count = RoommateApplication.objects.filter(
        applicant=request.user,
        status='pending'
    ).count()

    saved_posts_count = RoommateFavourite.objects.filter(
        user=request.user
    ).count()

    return render(request, 'roommate/roommate_dashboard.html', {
        'user_posts': user_posts,
        'received_applications': received_applications,
        'my_applications': my_applications,
        'saved_posts': saved_posts,
        'total_posts': total_posts,
        'open_posts_count': open_posts_count,
        'pending_received_count': pending_received_count,
        'pending_my_applications_count': pending_my_applications_count,
        'saved_posts_count': saved_posts_count,
    })


@login_required(login_url='/login/')
def toggle_favourite(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    if request.method == 'POST':
        favourite = RoommateFavourite.objects.filter(
            user=request.user,
            roommate_post=post
        ).first()

        if favourite:
            favourite.delete()

            messages.success(
                request,
                "Removed from favourites."
            )
            
        else:
            RoommateFavourite.objects.create(
                user=request.user,
                roommate_post=post
            )

            messages.success(
                  request,
                  "Added to favourites."
            )

    next_url = request.POST.get('next', 'roommate_list')

    return redirect(next_url)


@login_required(login_url='/login/')
def saved_roommate_posts(request):
    favourites = RoommateFavourite.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'roommate/saved_roommate_posts.html', {
        'favourites': favourites
    })

from django.http import JsonResponse
from django.utils.dateformat import format

@login_required(login_url='/login/')
def get_chat_messages(request, application_id):
    application = get_object_or_404(
        RoommateApplication,
        id=application_id
    )

    # Only applicant and coordinator can view the chat
    if (
        request.user != application.applicant and
        request.user != application.roommate_post.created_by
    ):
        return JsonResponse(
            {"error": "Permission denied"},
            status=403
        )

    messages = application.messages.all()

    data = []

    for msg in messages:
        data.append({
            "sender": (
                "You"
                if msg.sender == request.user
                else msg.sender.username
            ),
            "is_me": msg.sender == request.user,
            "message": msg.message,
            "time": format(msg.created_at, "d M Y, h:i A")
        })

    return JsonResponse(data, safe=False)

@login_required(login_url='/login/')
def send_chat_message(request, application_id):

    application = get_object_or_404(
        RoommateApplication,
        id=application_id
    )

    if request.method == "POST":

        message = request.POST.get("message")

        if message:

            RoommateMessage.objects.create(
                application=application,
                sender=request.user,
                message=message
            )

        return JsonResponse({
            "success": True
        })

    return JsonResponse({
        "success": False
    })