from django.shortcuts import render, redirect, get_object_or_404
from .models import RoommatePost
from django.contrib.auth.decorators import login_required


@login_required
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
            created_by=request.user
        )

        return redirect('roommate_list')

    return render(request, 'roommate/add_roommate.html')


def roommate_list(request):
    posts = RoommatePost.objects.all()
    return render(request, 'roommate/roommate_list.html', {'posts': posts})


@login_required
def delete_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id, created_by=request.user)
    post.delete()
    return redirect('roommate_list')


@login_required
def edit_roommate(request, id):
    post = get_object_or_404(RoommatePost, id=id, created_by=request.user)

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