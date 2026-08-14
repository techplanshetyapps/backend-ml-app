import codecs
import csv
from datetime import datetime
import requests
from django.core.management.base import BaseCommand
from govsim.models import TrafficSensorReading

class Command(BaseCommand):
    help = "Stream and seed traffic sensor readings directly from Hugging Face"

    def handle(self, *args, **kwargs):
        url = "https://huggingface.co/datasets/yatsbm/TrafficFresh/resolve/main/closure_tasks/traffic_lane_closure_split_data/associated_sensors/fwy_dir_I15-N.csv"

        self.stdout.write("Connecting to Hugging Face and streaming sensor data...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        reader = csv.DictReader(codecs.iterdecode(response.iter_lines(), 'utf-8'))

        batch = []
        count = 0

        for row in reader:
            try:
                batch.append(TrafficSensorReading(
                    hour=datetime.fromisoformat(row.get('hour') or row.get('timestamp')),
                    sensor_id=str(row.get('sensor_id', '')),
                    occupancy_pct=float(row['occupancy_pct']) if row.get('occupancy_pct') else None,
                    speed_mph=float(row['speed_mph']) if row.get('speed_mph') else None,
                    lane1_occ=float(row['lane1_occ']) if row.get('lane1_occ') else None,
                    lane1_speed=float(row['lane1_speed']) if row.get('lane1_speed') else None,
                    lane2_occ=float(row['lane2_occ']) if row.get('lane2_occ') else None,
                    lane2_speed=float(row['lane2_speed']) if row.get('lane2_speed') else None,
                    lane3_occ=float(row['lane3_occ']) if row.get('lane3_occ') else None,
                    lane3_speed=float(row['lane3_speed']) if row.get('lane3_speed') else None,
                    lane4_occ=float(row['lane4_occ']) if row.get('lane4_occ') else None,
                    lane4_speed=float(row['lane4_speed']) if row.get('lane4_speed') else None,
                    lane5_occ=float(row['lane5_occ']) if row.get('lane5_occ') else None,
                    lane5_speed=float(row['lane5_speed']) if row.get('lane5_speed') else None,
                    fwy=row.get('fwy', ''),
                    district=int(row['district']) if row.get('district') else 0,
                    county=row.get('county', ''),
                    city=row.get('city', ''),
                    ca_pm=row.get('ca_pm') or None,
                    abs_pm=float(row['abs_pm']) if row.get('abs_pm') else None,
                    length=float(row['length']) if row.get('length') else None,
                    name=row.get('name', ''),
                    lanes=int(row['lanes']) if row.get('lanes') else None,
                    type=row.get('type', ''),
                    sensor_type=row.get('sensor_type', ''),
                ))

                if len(batch) >= 1000:
                    TrafficSensorReading.objects.bulk_create(batch)
                    count += len(batch)
                    self.stdout.write(f"Processed {count} sensor records...")
                    batch = []
            except Exception as e:
                continue

        if batch:
            TrafficSensorReading.objects.bulk_create(batch)
            count += len(batch)

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded a total of {count} traffic sensor records!"))