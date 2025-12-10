from src.application.lead_collector import LeadCollector
from src.application.lead_classifier import LeadClassifier
from src.infrastructure.external.csv_exporter import CsvExporter


def run_cli():
    area = input("Area (e.g. 'Luton, UK'): ").strip()
    keyword = input("Keyword (e.g. 'eyelash extensions'): ").strip()

    collector = LeadCollector()
    classifier = LeadClassifier()
    exporter = CsvExporter()

    print(f"\n[INFO] Collecting leads for area='{area}', keyword='{keyword}'...")
    leads = collector.collect_leads(area_name=area, keyword=keyword)

    with_web, without_web = classifier.split_by_website(leads)

    print(f"[INFO] Total leads: {len(leads)}")
    print(f"[INFO] With website: {len(with_web)}")
    print(f"[INFO] Without website: {len(without_web)}")

    safe_keyword = keyword.replace(" ", "_").lower()
    safe_area = area.replace(" ", "_").lower()

    exporter.export(f"output/{safe_area}_{safe_keyword}_with_website.csv", with_web)
    exporter.export(f"output/{safe_area}_{safe_keyword}_without_website.csv", without_web)
    print("\n[INFO] Lead collection and export completed.")