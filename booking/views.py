from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Case, Count, F, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm
from .models import Creature, TimeSlot


def _available_time_slots_queryset():
    weekday_order = Case(
        When(weekday=TimeSlot.Weekday.MONDAY, then=Value(1)),
        When(weekday=TimeSlot.Weekday.TUESDAY, then=Value(2)),
        When(weekday=TimeSlot.Weekday.WEDNESDAY, then=Value(3)),
        When(weekday=TimeSlot.Weekday.THURSDAY, then=Value(4)),
        When(weekday=TimeSlot.Weekday.FRIDAY, then=Value(5)),
        When(weekday=TimeSlot.Weekday.SATURDAY, then=Value(6)),
        When(weekday=TimeSlot.Weekday.SUNDAY, then=Value(7)),
        default=Value(99),
        output_field=IntegerField(),
    )

    return (
        TimeSlot.objects.filter(is_active=True)
        .annotate(
            weekday_order=weekday_order,
            reservation_count_db=Count("reservations"),
            available_capacity=F("max_capacity") - Count("reservations"),
        )
        .filter(available_capacity__gt=0)
        .order_by("weekday_order", "start_time")
    )


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
        request.session.pop("selected_time_slot_id", None)
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

    available_time_slots = _available_time_slots_queryset()
    selected_time_slot_id = request.session.get("selected_time_slot_id")

    if request.method == "POST":
        time_slot_id = request.POST.get("time_slot_id")
        time_slot = get_object_or_404(available_time_slots, pk=time_slot_id)

        request.session["selected_time_slot_id"] = time_slot.id
        request.session.modified = True

        messages.success(
            request,
            "Horario seleccionado correctamente. Revisa el resumen antes de confirmar.",
        )
        return redirect("booking:confirm_reservation")

    context = {
        "selected_creature": selected_creature,
        "time_slots": available_time_slots,
        "selected_time_slot_id": selected_time_slot_id,
    }
    return render(request, "booking/choose_time_slot.html", context)


@login_required
def confirm_reservation(request):
    selected_creature_id = request.session.get("selected_creature_id")
    selected_time_slot_id = request.session.get("selected_time_slot_id")

    if not selected_creature_id:
        messages.error(request, "Primero debes elegir una criatura.")
        return redirect("booking:choose_creature")

    if not selected_time_slot_id:
        messages.error(request, "Primero debes elegir un horario.")
        return redirect("booking:choose_time_slot")

    selected_creature = get_object_or_404(
        Creature.objects.filter(is_available=True),
        pk=selected_creature_id,
    )

    selected_time_slot = _available_time_slots_queryset().filter(
        pk=selected_time_slot_id
    ).first()

    if not selected_time_slot:
        request.session.pop("selected_time_slot_id", None)
        request.session.modified = True
        messages.error(
            request,
            "Ese horario ya no está disponible. Elige otro, por favor.",
        )
        return redirect("booking:choose_time_slot")

    context = {
        "selected_creature": selected_creature,
        "selected_time_slot": selected_time_slot,
    }
    return render(request, "booking/confirm_reservation.html", context)