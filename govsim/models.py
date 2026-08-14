from django.db import models
from django.core.validators import MinLengthValidator

class Ad(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    text = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

class TrafficSensorReading(models.Model):
    hour = models.DateTimeField()
    sensor_id = models.CharField(max_length=20)
    occupancy_pct = models.FloatField(null=True, blank=True)
    speed_mph = models.FloatField(null=True, blank=True)

    lane1_occ = models.FloatField(null=True, blank=True)
    lane1_speed = models.FloatField(null=True, blank=True)
    lane2_occ = models.FloatField(null=True, blank=True)
    lane2_speed = models.FloatField(null=True, blank=True)
    lane3_occ = models.FloatField(null=True, blank=True)
    lane3_speed = models.FloatField(null=True, blank=True)
    lane4_occ = models.FloatField(null=True, blank=True)
    lane4_speed = models.FloatField(null=True, blank=True)
    lane5_occ = models.FloatField(null=True, blank=True)
    lane5_speed = models.FloatField(null=True, blank=True)

    fwy = models.CharField(max_length=20)          # e.g. "I10-E"
    district = models.IntegerField()
    county = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    ca_pm = models.CharField(max_length=20, null=True, blank=True)   # postmile code
    abs_pm = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=100)         # e.g. "LINCOLN"
    lanes = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50)           # e.g. "Mainline"
    sensor_type = models.CharField(max_length=50)     # e.g. "loops"

    class Meta:
        indexes = [
            models.Index(fields=['sensor_id', 'hour']),
            models.Index(fields=['fwy', 'county']),
        ]

    def __str__(self):
        return f"{self.fwy} {self.name} @ {self.hour}"
