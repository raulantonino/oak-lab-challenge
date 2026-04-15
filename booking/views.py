from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm
from .models import Creature


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
    creatures = Creature.objects.filter(is_available=True).order_by("name")
    selected_creature_id = request.session.get("selected_creature_id")

    if request.method == "POST":
        creature_id = request.POST.get("creature_id")
        creature = get_object_or_404(creatures, pk=creature_id)

        request.session["selected_creature_id"] = creature.id
        request.session.modified = True

        messages.success(
            request,
            f"Elegiste a {creature.name}. Ahora selecciona un horario disponible.",
        )
        return redirect("booking:choose_time_slot")

    context = {
        "creatures": creatures,
        "selected_creature_id": selected_creature_id,
    }
    return render(request, "booking/choose_creature.html", context)


@login_required
def choose_time_slot(request):
    selected_creature_id = request.session.get("selected_creature_id")

    if not selected_creature_id:
        messages.error(request, "Primero debes elegir una criatura.")
        return redirect("booking:choose_creature")

    selected_creature = get_object_or_404(
        Creature.objects.filter(is_available=True),
        pk=selected_creature_id,
    )

    context = {
        "selected_creature": selected_creature,
    }
    return render(request, "booking/choose_time_slot.html", context)