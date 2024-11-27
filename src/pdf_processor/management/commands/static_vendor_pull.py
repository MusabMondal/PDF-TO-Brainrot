import Helper

from pathlib import Path
from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand

STATICFILES_VENDOR_DIR = getattr(settings, "STATICFILES_VENDOR_DIR", None)
if STATICFILES_VENDOR_DIR is None:
    raise ValueError("STATICFILES_VENDOR_DIR setting is not defined in settings.")

VENDOR_STATIC = {
    "saas-theme.min.css" : "https://raw.githubusercontent.com/codingforentrepreneurs/SaaS-Foundations/main/src/staticfiles/theme/saas-theme.min.css",
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    "flowbite.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map",
}

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Downloading vendor static files")

        completed_download = []
        for file, url in VENDOR_STATIC.items():
            out_path = Path(STATICFILES_VENDOR_DIR) / file
            is_successful = Helper.download_to_local(url, out_path)
            # print(file, url, out_path)
            if is_successful:
                completed_download.append(url)
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download {file}"))

        if set(completed_download) == set(VENDOR_STATIC.values()):
            self.stdout.write(self.style.SUCCESS("All vendor static files are downloaded"))
        else:
            self.stdout.write(self.style.WARNING("Some vendor static files were not downloaded"))