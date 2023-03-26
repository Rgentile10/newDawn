from django.shortcuts import render, redirect
from .models import Profile
from .forms import MessageForm


def dashboard(request):
    form = MessageForm(request.POST or None)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            messagee = form.save(commit=False)
            messagee.user = request.user
            messagee.save()
    return render(request, "whoshonest/dashboard.html", {"form": form})


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "whoshonest/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "whoshonest/profile.html", {"profile": profile})