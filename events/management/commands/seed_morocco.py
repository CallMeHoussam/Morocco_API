from django.core.management.base import BaseCommand
from django.utils.text import slugify
from events.models import City, Category

CITIES = [
    ("Casablanca", "Casablanca-Settat"),
    ("Rabat", "Rabat-Salé-Kénitra"),
    ("Fès", "Fès-Meknès"),
    ("Marrakech", "Marrakech-Safi"),
    ("Tangier", "Tanger-Tétouan-Al Hoceïma"),
    ("Agadir", "Souss-Massa"),
    ("Oujda", "Oriental"),
    ("Laayoune", "Laâyoune-Sakia El Hamra"),
]
CATEGORIES = ["Culture", "Sport", "Education", "Conference", "Festival", "Job Fair"]

class Command(BaseCommand):
    help = "Seeds Moroccan cities and categories."

    def handle(self, *args, **options):
        for name, region in CITIES:
            City.objects.get_or_create(name=name, region=region, slug=slugify(name))
        for name in CATEGORIES:
            Category.objects.get_or_create(name=name, slug=slugify(name))
        self.stdout.write(self.style.SUCCESS("Seeded cities and categories."))
