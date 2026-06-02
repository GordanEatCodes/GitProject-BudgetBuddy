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
        post.save()

        return redirect('roommate_list')

    return render(request, 'roommate/edit_roommate.html', {'post': post})


def match_roommates(request, id):
    current_user_post = get_object_or_404(RoommatePost, id=id)
    all_posts = RoommatePost.objects.exclude(id=id)

    results = []

    for post in all_posts:
        score = 0

        if current_user_post.location.lower() == post.location.lower():
            score += 3

        budget_diff = abs(float(current_user_post.budget) - float(post.budget))

        if budget_diff <= 100:
            score += 3
        elif budget_diff <= 300:
            score += 1

        common_words = set(current_user_post.description.lower().split()) & set(post.description.lower().split())
        score += len(common_words)

        results.append((post, score))

    results.sort(key=lambda x: x[1], reverse=True)

    return render(request, 'roommate/match.html', {
        'current': current_user_post,
        'matches': results
    })