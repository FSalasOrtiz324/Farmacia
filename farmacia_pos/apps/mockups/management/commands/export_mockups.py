"""Exporta las maquetas como sitio estático (p. ej. GitHub Pages).

Cada pantalla queda en <salida>/<slug>/index.html con enlaces relativos, para que el
sitio funcione bajo cualquier subruta. Solo exporta datos ficticios.
"""

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import Client

from apps.mockups.views import SCREENS, STANDALONE

PREFIX = "/maquetas/"
REDIRECT = (
    '<!doctype html><meta charset="utf-8"><title>Maqueta Farmacia</title>'
    '<meta http-equiv="refresh" content="0; url={target}"><a href="{target}">Abrir maqueta</a>'
)


class Command(BaseCommand):
    help = "Exporta las maquetas de interfaz a HTML estático."

    def add_arguments(self, parser):
        parser.add_argument("output", type=Path)
        parser.add_argument("--start", default="login", help="Pantalla de entrada del sitio")

    def handle(self, output: Path, start: str, **options):
        if not settings.DEBUG:
            raise CommandError("Las maquetas solo existen con DEBUG=true.")
        client = Client(HTTP_HOST=(settings.ALLOWED_HOSTS or ["localhost"])[0])
        output.mkdir(parents=True, exist_ok=True)
        for slug in [*SCREENS, *STANDALONE]:
            response = client.get(f"{PREFIX}{slug}/")
            if response.status_code != 200:
                raise CommandError(f"{slug}: HTTP {response.status_code}")
            html = response.content.decode()
            # Páginas a un nivel de profundidad: /maquetas/x/ -> ../x/ ; /maquetas/ -> ../inicio/
            html = html.replace(f'"{PREFIX}"', '"../inicio/"').replace(f'"{PREFIX}', '"../')
            page = output / slug / "index.html"
            page.parent.mkdir(exist_ok=True)
            page.write_text(html, encoding="utf-8")
        (output / "index.html").write_text(REDIRECT.format(target=f"{start}/"), encoding="utf-8")
        (output / ".nojekyll").write_text("")
        self.stdout.write(self.style.SUCCESS(f"{len(SCREENS) + len(STANDALONE)} pantallas en {output}"))
