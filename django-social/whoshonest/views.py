from django.shortcuts import render, redirect
from .models import Profile
from .forms import MessageForm

import openai

API_KEY = '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'
openai.api_key = API_KEY

model_id = 'gpt-3.5-turbo'

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


def dashboard(request):
    form = MessageForm(request.POST)
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