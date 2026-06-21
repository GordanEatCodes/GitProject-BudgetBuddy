from django.shortcuts import render, redirect, get_object_or_404
from .models import RoommatePost


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
        )

        return redirect('roommate_list')

    return render(request, 'roommate/add_roommate.html')


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
        posts = posts.order_by('-created_at')  # default: newest first

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

def delete_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id)

    if request.method == 'POST':
        post.delete()
        return redirect('roommate_list')

    return render(request, 'roommate/confirm_delete.html', {'post': post})


def edit_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id)

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

        current_location = current_user_post.location.lower().strip()
        post_location = post.location.lower().strip()

        if current_location == post_location:
            score += 25
            reasons.append("Same location")
        elif current_location in post_location or post_location in current_location:
            score += 15
            reasons.append("Similar location")
        else:
            reasons.append("Different location")

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

        current_words = set(current_user_post.description.lower().split()) - stop_words
        post_words = set(post.description.lower().split()) - stop_words

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