from django.shortcuts import render, redirect, get_object_or_404
from .models import List
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UpdateDetailForm, UpdateProfileForm, UpdateUserForm


# Create your views here.

@login_required
def home(request):
    if request.method == "POST":
        if request.POST.get("list") == "":
            all_list = List.objects.filter(author=request.user)
            return render(request, "home.html", {"all_list": all_list})
        else:
            new_list = request.POST.get("list")
            List.objects.create(content=new_list, author=request.user)
            all_list = List.objects.filter(author=request.user)
            messages.success(request, "New list Successfuly added!")
            return render(request, "home.html", {"all_list": all_list})

    else:
        all_list = List.objects.filter(author=request.user)
        return render(request, "home.html", {"all_list": all_list})

def delete(request, pk):
    item = List.objects.get(pk=pk)
    print(item.pk)
    item.delete()
    messages.success(request, "List Successfuly deleted")
    return redirect("home")

def complete(request, pk):
    item = List.objects.get(pk=pk)
    print("{} | {} ".format(item.content, item.pk))
    print(request.user.username)
    item.completed = True
    item.save()
    messages.success(request, "Change saved")
    return redirect("home")

def uncomplete(request, pk):
    item = List.objects.get(pk=pk)
    print("{} | {} ".format(item.content, item.pk))
    item.completed = False
    item.save()
    messages.success(request, "Change saved")
    return redirect("home")

def detail(request, pk):
    item = get_object_or_404(List, pk=pk)
    if request.method == "POST":
        form = UpdateDetailForm(request.POST)
        if form.is_valid():
            item.content = request.POST.get("content")
            item.save()
            messages.success(request, "List Updated!")
            print(item.content)
            return render(request, "detail.html", {"form": form, "item": item})
    else:
        form = UpdateDetailForm()
        return render(request, "detail.html", {"form": form, "item": item})

@login_required()
def false_list(request):
    lists = List.objects.filter(author=request.user, completed=False)
    print(lists)
    return render(request, "falselist.html", {"lists": lists})

@login_required()
def done_list(request):
    lists = List.objects.filter(author=request.user, completed=True)
    print(lists)
    return render(request, "truelist.html", {"lists": lists})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been create!")
            return redirect("login")
    else:
        form = UserRegistrationForm
    return render(request, "register.html", {"form": form})

@login_required()
def profile(request):
    if request.method == "POST":
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, "profile.html", {"u_form": u_form, "p_form": p_form})












