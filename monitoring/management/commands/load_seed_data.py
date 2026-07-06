from datetime import datetime
from django.core.management.base import BaseCommand
from monitoring.models import Station, Observation


class Command(BaseCommand):
    help = "Загружает тестовые данные (3 станции, 18 наблюдений) — аналог seed_data.sql"

    def handle(self, *args, **options):
        Observation.objects.all().delete()
        Station.objects.all().delete()

        stations_data = [
            ("Station-01", "Бишкек, Центр", 42.8746, 74.5698, "2025-03-10"),
            ("Station-02", "Бишкек, Восточный", 42.8800, 74.6300, "2025-05-22"),
            ("Station-03", "Кант", 42.8900, 74.8500, "2025-07-01"),
        ]
        stations = {}
        for name, location, lat, lon, installed in stations_data:
            s = Station.objects.create(
                name=name, location=location, latitude=lat, longitude=lon, installed_at=installed
            )
            stations[name] = s

        observations_data = [
            ("Station-01", "2026-06-29 08:00", "temperature", 18.5, "°C"),
            ("Station-01", "2026-06-29 08:00", "humidity", 55.0, "%"),
            ("Station-01", "2026-06-29 08:00", "pressure", 1012.3, "hPa"),
            ("Station-01", "2026-06-30 08:00", "temperature", 19.2, "°C"),
            ("Station-01", "2026-06-30 08:00", "humidity", 53.5, "%"),
            ("Station-01", "2026-06-30 08:00", "pm25", 24.0, "µg/m3"),
            ("Station-01", "2026-07-01 08:00", "temperature", 21.0, "°C"),
            ("Station-01", "2026-07-01 08:00", "humidity", 50.0, "%"),
            ("Station-02", "2026-06-29 08:00", "temperature", 17.8, "°C"),
            ("Station-02", "2026-06-29 08:00", "pm25", 31.5, "µg/m3"),
            ("Station-02", "2026-06-30 08:00", "temperature", 18.9, "°C"),
            ("Station-02", "2026-06-30 08:00", "pm25", 29.2, "µg/m3"),
            ("Station-02", "2026-07-01 08:00", "temperature", 20.1, "°C"),
            ("Station-02", "2026-07-01 08:00", "humidity", 48.0, "%"),
            ("Station-03", "2026-07-01 09:00", "temperature", 22.4, "°C"),
            ("Station-03", "2026-07-01 09:00", "humidity", 45.0, "%"),
            ("Station-03", "2026-07-01 09:00", "pressure", 1010.1, "hPa"),
            ("Station-03", "2026-07-01 09:00", "pm25", 18.7, "µg/m3"),
        ]
        for station_name, observed_at, parameter, value, unit in observations_data:
            Observation.objects.create(
                station=stations[station_name],
                observed_at=datetime.strptime(observed_at, "%Y-%m-%d %H:%M"),
                parameter=parameter,
                value=value,
                unit=unit,
            )

        self.stdout.write(self.style.SUCCESS(
            f"Загружено станций: {Station.objects.count()}, наблюдений: {Observation.objects.count()}"
        ))
