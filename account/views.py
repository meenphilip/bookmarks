from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from django.contrib import messages
from actions.utils import create_action


# login View
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "account/login.html", context)


# logout view
def user_logout(request):
    logout(request)
    return redirect("login")


# Authourized users only
@login_required
def dashboard(request):
    context = {"section": "dashboard"}
    return render(request, "account/dashboard.html", context)


# User Registration Form
def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user obj avoid saving it
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # save user obj
            new_user.save()
            # create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, "has created an account")
            context = {"new_user": new_user}
            return render(request, "account/register_done.html", context)
    else:
        user_form = UserRegistrationForm()
    context = {"user_form": user_form}
    return render(request, "account/register.html", context)


# Edit profile
@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # message
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "account/edit.html", context)


# Create list view for user profiles
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    context = {"section": "people", "users": users}
    return render(request, "account/user/list.html", context)


# Create detail view for user profiles
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    context = {"section": "people", "user": user}
    return render(request, "account/user/detail.html", context)


# implement follow/unfollow feature
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, "is following", user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except user.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})
