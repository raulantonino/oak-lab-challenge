from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignUpForm


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("booking:choose_creature")
    return redirect("booking:login")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("booking:choose_creature")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Tu cuenta fue creada con éxito. ¡Bienvenido al laboratorio del Profesor Oak!",
            )
            return redirect("booking:choose_creature")

        messages.error(request, "Revisa los datos del formulario.")

    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def choose_creature(request):
    return render(request, "booking/choose_creature.html")