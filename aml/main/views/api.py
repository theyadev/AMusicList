from django.forms import Form
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate

from ..forms import LoginForm, SignupForm

from ..models import Song, Action, User, Lists, Activities


def logout_api(request):
    try:
        redirect_url = request.GET["to"]
    except:
        redirect_url = "/"

    if request.user.is_authenticated:
        logout(request)

    return redirect(redirect_url)


def login_api(request):
    if request.method == "POST":
        try:
            redirect_url = request.GET["to"]
        except:
            redirect_url = "/"

        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(redirect_url)

    return redirect("/login")


def signup_api(request):
    if request.method == "POST":
        try:
            redirect_url = request.GET["to"]
        except:
            redirect_url = "/"

        form = SignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]

            if password != confirm_password:
                return redirect("/signup")

            if len(User.objects.filter(email=email)) > 0:
                return redirect("/signup")

            try:
                user = User.objects.create_user(username, email, password)
            except:
                return redirect("/signup")

            user.save()

            log = authenticate(request, username=email, password=password)

            if log is not None:
                login(request, log)
                return redirect(redirect_url)

            print(user)
    return redirect("/signup")


def add_to_list(request, songId):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            song = Song.objects.get(id=songId)
        except Song.DoesNotExist:
            return render(request, "404.html")

        try:
            list_entry = Lists.objects.get(user=request.user, song=song)
            list_entry.delete()
            action = Action.objects.get(name="REMOVED")
        except:
            list_entry = Lists(user=request.user, song=song, favourite=False)
            list_entry.save()
            action = Action.objects.get(name="ADDED")

        activity = Activities(song=song, user=request.user, action=action)
        activity.save()

    return redirect("/song/" + str(songId))


def add_to_favourite(request, songId):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            song = Song.objects.get(id=songId)
        except Song.DoesNotExist:
            return render(request, "404.html")

        try:
            list_entry = Lists.objects.get(user=request.user, song=song)
            list_entry.favourite = not list_entry.favourite

            list_entry.save()

            action = Action.objects.get(name="FAVOURITE")
            activity = Activities(song=song, user=request.user, action=action)
            activity.save()
        except:
            return redirect("/song/" + str(songId))

    return redirect("/song/" + str(songId))

def add_friend(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            redirect_url = request.GET["to"]
        except:
            redirect_url = "/"
        
        form = Form(request.POST)

        try:
            id = form.data['id']
            user = User.objects.get(id=id)

            if request.user.follows.filter(id=user.id).exists():
                request.user.follows.remove(user)
            else:
                request.user.follows.add(user)
        except:
            return redirect('/404')

        return redirect(redirect_url)