from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.core.mail import EmailMessage

from .forms import UserRegistrationForm, UpdateDetailForm, UpdateProfileForm, UpdateUserForm
from .models import List


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
    item = get_object_or_404(List, pk=pk)
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


# Registration Area<=========================================================================>
# REGISTRATION SITE

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data["email"]
            if not User.objects.filter(email=email).exists():
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_subject = "Activate Your Account"
                message = render_to_string('activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(email_subject, message, to=[email])
                email.send()
                return HttpResponse("We have sent you an email,please confirm your email adress")
            else:
                messages.info(request, "The email is already in used")
                return render(request, "register.html", {"form": form})
    else:
        form = UserRegistrationForm
    return render(request, "register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("login")
    else:
        return HttpResponse('invalid token')


# <==========================================================================================>
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
