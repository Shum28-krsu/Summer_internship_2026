from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    location = models.CharField(max_length=200, verbose_name="Расположение")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    installed_at = models.DateField(verbose_name="Дата установки")

    class Meta:
        verbose_name = "Станция"
        verbose_name_plural = "Станции"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def last_observations(self):
        """Последнее наблюдение по каждому параметру для этой станции."""
        results = []
        for param, _ in Observation.PARAMETER_CHOICES:
            obs = self.observations.filter(parameter=param).order_by("-observed_at").first()
            if obs:
                results.append(obs)
        return results


class Observation(models.Model):
    PARAMETER_CHOICES = [
        ("temperature", "Температура"),
        ("humidity", "Влажность"),
        ("pressure", "Давление"),
        ("pm25", "PM2.5"),
    ]

    UNIT_BY_PARAMETER = {
        "temperature": "°C",
        "humidity": "%",
        "pressure": "hPa",
        "pm25": "µg/m3",
    }

    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="observations", verbose_name="Станция"
    )
    observed_at = models.DateTimeField(verbose_name="Дата и время наблюдения")
    parameter = models.CharField(max_length=20, choices=PARAMETER_CHOICES, verbose_name="Параметр")
    value = models.FloatField(verbose_name="Значение")
    unit = models.CharField(max_length=20, verbose_name="Единица измерения")

    class Meta:
        verbose_name = "Наблюдение"
        verbose_name_plural = "Наблюдения"
        ordering = ["-observed_at"]
        indexes = [
            models.Index(fields=["station"]),
            models.Index(fields=["observed_at"]),
        ]

    def __str__(self):
        return f"{self.station.name} — {self.get_parameter_display()}: {self.value}{self.unit}"

    def save(self, *args, **kwargs):
        if not self.unit:
            self.unit = self.UNIT_BY_PARAMETER.get(self.parameter, "")
        super().save(*args, **kwargs)
