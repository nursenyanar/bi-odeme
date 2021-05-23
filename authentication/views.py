from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('siparis')

    next=request.GET.get("next",None)
    msg=""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("siparis")
        else:
            msg = "Kullanıcı adı veya parola yanlış"
    context = {
        "hata": msg
    }
    return render(request, "login.html", context)
