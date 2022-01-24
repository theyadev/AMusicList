from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate

from .forms import LoginForm, SignupForm

from .models import Song, User

def index(request):
    return HttpResponse("Hello, world. You're at the main index.")

def detail(request, songId):
    try:
        song = Song.objects.get(id=songId)
    except Song.DoesNotExist:
        return render(request, "main/404.html")

    context = {'song': song}

    return render(request, 'main/detail.html', context)

def staff(request, songId):
    try:
        song = Song.objects.get(id=songId)
    except Song.DoesNotExist:
        return render(request, "main/404.html")

    staffs = song.staffs.all()

    return render(request, 'main/staffs.html', {
        'staffs': staffs
    })

def logout_view(request):
    if request.method == "POST":
        redirect_url = request.GET['to']

        if request.user.is_authenticated:
            logout(request)

        return redirect("/" + redirect_url)
    
    return render(request, "main/404.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")

    context = {'form': LoginForm()}

    return render(request, "main/login.html", context)

def signup_view(request):
    context = {'form': SignupForm()}

    # if request.user.is_authenticated:
    #     return redirect("/")
    # el
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                return render(request, "main/signup.html", context)

            if len(User.objects.filter(email=email)) > 0:
                return render(request, "main/signup.html", context)

            try:
                user = User.objects.create_user(username, email, password)
            except:
                return render(request, "main/signup.html", context)

            user.save()

            log = authenticate(request, username=email, password=password)

            if log is not None:
                login(request, log)
                return redirect("/")

            print(user)
            return redirect("/")

    return render(request, "main/signup.html", context)