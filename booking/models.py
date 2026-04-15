from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class Creature(models.Model):
    class ElementType(models.TextChoices):
        FIRE = "fire", "Fuego"
        GRASS = "grass", "Planta"
        WATER = "water", "Agua"

    name = models.CharField(max_length=50, unique=True)
    element_type = models.CharField(max_length=10, choices=ElementType.choices)
    description = models.TextField()
    emoji = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Creature"
        verbose_name_plural = "Creatures"

    def __str__(self):
        return f"{self.emoji} {self.name}"


class TimeSlot(models.Model):
    class Weekday(models.TextChoices):
        MONDAY = "monday", "Lunes"
        TUESDAY = "tuesday", "Martes"
        WEDNESDAY = "wednesday", "Miércoles"
        THURSDAY = "thursday", "Jueves"
        FRIDAY = "friday", "Viernes"
        SATURDAY = "saturday", "Sábado"
        SUNDAY = "sunday", "Domingo"

    weekday = models.CharField(max_length=12, choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_capacity = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["weekday", "start_time"]
        verbose_name = "Time slot"
        verbose_name_plural = "Time slots"
        constraints = [
            models.UniqueConstraint(
                fields=["weekday", "start_time", "end_time"],
                name="unique_time_slot_block",
            ),
            models.CheckConstraint(
                condition=Q(max_capacity__gt=0),
                name="timeslot_max_capacity_gt_0",
            ),
            models.CheckConstraint(
                condition=Q(end_time__gt=F("start_time")),
                name="timeslot_end_after_start",
            ),
        ]

    def __str__(self):
        return (
            f"{self.get_weekday_display()} "
            f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        )

    @property
    def reserved_count(self):
        return self.reservations.count()

    @property
    def remaining_capacity(self):
        return self.max_capacity - self.reserved_count

    @property
    def is_full(self):
        return self.remaining_capacity <= 0


class Reservation(models.Model):
    trainer = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservation",
    )
    creature = models.ForeignKey(
        Creature,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def __str__(self):
        return (
            f"{self.trainer.username} - "
            f"{self.creature.name} - "
            f"{self.time_slot}"
        )

    def clean(self):
        super().clean()

        if self.time_slot and self.time_slot.remaining_capacity <= 0:
            raise ValidationError(
                {"time_slot": "Este horario ya no tiene cupos disponibles."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)