import csv
from pathlib import Path
from typing import Iterable

from src.domain.models import BusinessLead


class CsvExporter:
    def export(self, filename: str | Path, leads: Iterable[BusinessLead]) -> None:
        """
        Export an iterable of BusinessLead objects to a CSV file.
        """
        leads = list(leads)
        if not leads:
            # You may choose to still create an empty file if you prefer
            print(f"[CsvExporter] No leads to export for {filename}")
            return

        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = [
            "name",
            "address",
            "phone",
            "website",
            "google_maps_url",
            "rating",
            "user_ratings_total",
            "place_id",
        ]

        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for lead in leads:
                writer.writerow(
                    {
                        "name": lead.name,
                        "address": lead.address,
                        "phone": lead.phone or "",
                        "website": lead.website or "",
                        "google_maps_url": lead.google_maps_url or "",
                        "rating": lead.rating if lead.rating is not None else "",
                        "user_ratings_total": (
                            lead.user_ratings_total if lead.user_ratings_total is not None else ""
                        ),
                        "place_id": lead.place_id or "",
                    }
                )

        print(f"[CsvExporter] Exported {len(leads)} leads to {path}")
