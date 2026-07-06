from django.contrib import admin
from .models import Station, Observation


class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 0
    fields = ("observed_at", "parameter", "value", "unit")
    ordering = ("-observed_at",)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "installed_at")
    search_fields = ("name", "location")
    inlines = [ObservationInline]


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ("station", "parameter", "value", "unit", "observed_at")
    list_filter = ("parameter", "station")
    search_fields = ("station__name",)
    date_hierarchy = "observed_at"
