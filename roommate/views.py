from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RoommatePost, RoommateApplication, RoommateMessage
import string


def normalize_text(text):
    """
    This function standardizes text before comparison.
    Example:
    'Cyberjaya.' -> 'cyberjaya'
    '  QUIET, clean! ' -> 'quiet clean'
    """
    if not text:
        return ""

    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = " ".join(text.split())

    return text


@login_required(login_url='/login/')
def add_roommate(request):
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

            cleanliness=request.POST.get('cleanliness', 'any'),
            sleep_schedule=request.POST.get('sleep_schedule', 'any'),
            study_preference=request.POST.get('study_preference', 'any'),
            smoking=request.POST.get('smoking', 'any'),
            pets=request.POST.get('pets', 'any'),

            # Store who created this roommate post
            created_by=request.user,
        )

        return redirect('roommate_list')

    return render(request, 'roommate/add_roommate.html')


def roommate_list(request):
    posts = RoommatePost.objects.all()

    location = request.GET.get('location')
    max_budget = request.GET.get('max_budget')
    sort = request.GET.get('sort')

    # Filter by location
    if location:
        posts = posts.filter(location__icontains=location)

    # Filter by maximum budget
    if max_budget:
        try:
            posts = posts.filter(budget__lte=float(max_budget))
        except ValueError:
            pass

    # Sort function
    if sort == 'oldest':
        posts = posts.order_by('created_at')
    elif sort == 'low_budget':
        posts = posts.order_by('budget')
    elif sort == 'high_budget':
        posts = posts.order_by('-budget')
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'roommate/roommate_list.html', {
        'posts': posts,
        'location': location,
        'max_budget': max_budget,
        'sort': sort,
    })


def roommate_detail(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    return render(request, 'roommate/roommate_detail.html', {
        'post': post
    })


@login_required(login_url='/login/')
def delete_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    # Only creator can delete own post
    if post.created_by != request.user:
        return redirect('roommate_detail', id=post.id)

    if request.method == 'POST':
        post.delete()
        return redirect('roommate_list')

    return render(request, 'roommate/confirm_delete.html', {'post': post})


@login_required(login_url='/login/')
def edit_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    # Only creator can edit own post
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

        post.cleanliness = request.POST.get('cleanliness', 'any')
        post.sleep_schedule = request.POST.get('sleep_schedule', 'any')
        post.study_preference = request.POST.get('study_preference', 'any')
        post.smoking = request.POST.get('smoking', 'any')
        post.pets = request.POST.get('pets', 'any')

        post.save()

        return redirect('roommate_list')

    return render(request, 'roommate/edit_roommate.html', {'post': post})


def match_roommates(request, id):
    current_user_post = get_object_or_404(RoommatePost, id=id)
    all_posts = RoommatePost.objects.exclude(id=id)

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

        # 4. Description keyword similarity - max 15
        current_description = normalize_text(current_user_post.description)
        post_description = normalize_text(post.description)

        current_words = set(current_description.split()) - stop_words
        post_words = set(post_description.split()) - stop_words

        common_words = current_words & post_words
        keyword_score = min(len(common_words) * 3, 15)

        score += keyword_score

        if common_words:
            reasons.append("Similar keywords: " + ", ".join(common_words))
        else:
            reasons.append("No strong keyword similarity")

        # Make sure percentage does not exceed 100
        match_percentage = min(score, 100)

        # Match label
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

    # Old posts may not have creator, so application is not allowed
    if post.created_by is None:
        return redirect('roommate_detail', id=post.id)

    # User cannot apply to own post
    if post.created_by == request.user:
        return redirect('roommate_detail', id=post.id)

    # Prevent duplicate application
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

        # Save first message into chat
        if message:
            RoommateMessage.objects.create(
                application=application,
                sender=request.user,
                message=message
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

    # Only post creator / coordinator can accept or reject
    if application.roommate_post.created_by != request.user:
        return redirect('roommate_list')

    # Only allow valid statuses
    if status not in ['pending', 'accepted', 'rejected']:
        return redirect('applications_received')

    if request.method == 'POST':
        application.status = status
        application.save()

    return redirect('applications_received')


@login_required(login_url='/login/')
def application_detail(request, application_id):
    application = get_object_or_404(RoommateApplication, id=application_id)

    is_applicant = application.applicant == request.user
    is_coordinator = application.roommate_post.created_by == request.user

    # Only applicant or coordinator can view the chat page
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