from .models import TrafficSensorReading

def traffic_stats(request):
    return {
        'total_traffic_events': TrafficSensorReading.objects.count(),
        'available_freeways': TrafficSensorReading.objects.values_list('fwy', flat=True).distinct(),
    }