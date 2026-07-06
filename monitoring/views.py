from django.db.models import Count, Min, Max, Avg
from django.shortcuts import render, get_object_or_404
from .models import Station, Observation


def stations_list(request):
    stations = Station.objects.all()
    return render(request, "monitoring/stations_list.html", {"stations": stations})


def station_detail(request, pk):
    station = get_object_or_404(Station, pk=pk)
    observations = station.observations.all()

    parameter = request.GET.get("parameter")
    date_from = request.GET.get("from")
    date_to = request.GET.get("to")

    if parameter:
        observations = observations.filter(parameter=parameter)
    if date_from:
        observations = observations.filter(observed_at__gte=date_from)
    if date_to:
        observations = observations.filter(observed_at__lte=date_to)

    context = {
        "station": station,
        "observations": observations,
        "last_observations": station.last_observations(),
        "parameter_choices": Observation.PARAMETER_CHOICES,
        "selected_parameter": parameter or "",
        "date_from": date_from or "",
        "date_to": date_to or "",
    }
    return render(request, "monitoring/station_detail.html", context)


def dashboard(request):
    summary = (
        Observation.objects.values("parameter")
        .annotate(count=Count("id"), min_value=Min("value"), max_value=Max("value"), avg_value=Avg("value"))
        .order_by("parameter")
    )
    parameter_labels = dict(Observation.PARAMETER_CHOICES)
    for row in summary:
        row["label"] = parameter_labels.get(row["parameter"], row["parameter"])
        row["avg_value"] = round(row["avg_value"], 2) if row["avg_value"] is not None else None

    stations_count = Station.objects.count()
    observations_count = Observation.objects.count()

    return render(
        request,
        "monitoring/dashboard.html",
        {
            "summary": summary,
            "stations_count": stations_count,
            "observations_count": observations_count,
        },
    )
