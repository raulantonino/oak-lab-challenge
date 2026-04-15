from django.contrib import admin

from .models import Creature, Reservation, TimeSlot

admin.site.site_header = "Profesor Oak Admin"
admin.site.site_title = "Oak Lab Admin"
admin.site.index_title = "Gestión del laboratorio"


@admin.register(Creature)
class CreatureAdmin(admin.ModelAdmin):
    list_display = ("name", "element_type", "emoji", "is_available")
    list_filter = ("element_type", "is_available")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = (
        "weekday",
        "start_time",
        "end_time",
        "max_capacity",
        "remaining_capacity_display",
        "is_active",
    )
    list_filter = ("weekday", "is_active")
    ordering = ("weekday", "start_time")

    @admin.display(description="Cupos disponibles")
    def remaining_capacity_display(self, obj):
        return obj.remaining_capacity


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "trainer",
        "creature",
        "time_slot",
        "created_at",
    )
    list_filter = (
        "creature",
        "time_slot__weekday",
        "created_at",
    )
    search_fields = (
        "trainer__username",
        "creature__name",
    )
    ordering = ("-created_at",)
    list_select_related = ("trainer", "creature", "time_slot")
    readonly_fields = ("created_at",)