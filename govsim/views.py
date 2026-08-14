import os
import json
from django.conf import settings
from django.views.generic import ListView, TemplateView
from .models import Ad

# Basic Index View
class AdListView(ListView):
    model = Ad
    template_name = 'ad_list.html'
    context_object_name = 'ad_list'

# Notebook Dashboard View
class AutoMatrixDashboardView(TemplateView):
    template_name = 'traffic_matrix_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notebooks_data = []

        nb_files = [
            {'title': '01_vehicleClassificationTrafficPrediction.ipynb', 'type': 'Traffic Prediction Notebook'},
            {'title': '02_vehicleClassificationDeepLearing.ipynb', 'type': 'Deep Learning Notebook'},
            {'title': '03_trafficSpeedPredictionTimeSeries.ipynb', 'type': 'Time Series Analysis'},
            {'title': '04_trafficSpeedPredictionDeepLearning.ipynb', 'type': 'Deep Learning Notebook'},
            {'title': '05_3dMeshCars.ipynb', 'type': '3D Mesh Processing Notebook'}
        ]

        for item in nb_files:
            file_path = os.path.join(settings.BASE_DIR, 'static', item['title'])
            outputs_collected = []

            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        nb_content = json.load(f)
                        for cell in nb_content.get('cells', []):
                            if cell.get('cell_type') == 'code':
                                for output in cell.get('outputs', []):

                                    # 1. Capture standard text output
                                    if 'text' in output:
                                        outputs_collected.append({
                                            'type': 'text',
                                            'content': "".join(output['text'])
                                        })

                                    # 2. Capture rich data (text/plain, images, etc.)
                                    elif 'data' in output:
                                        data = output['data']

                                        # Check for PNG images
                                        if 'image/png' in data:
                                            img_str = "".join(data['image/png']).strip()
                                            outputs_collected.append({
                                                'type': 'image',
                                                'content': f"data:image/png;base64,{img_str}"
                                            })
                                        # Check for JPEG images
                                        elif 'image/jpeg' in data:
                                            img_str = "".join(data['image/jpeg']).strip()
                                            outputs_collected.append({
                                                'type': 'image',
                                                'content': f"data:image/jpeg;base64,{img_str}"
                                            })
                                        # Fallback to plain text output representation
                                        elif 'text/plain' in data:
                                            outputs_collected.append({
                                                'type': 'text',
                                                'content': "".join(data['text/plain'])
                                            })
                else:
                    outputs_collected = [{'type': 'text', 'content': f"File not found on server at: {file_path}"}]
            except Exception as e:
                outputs_collected = [{'type': 'text', 'content': f"Error parsing notebook execution logs: {str(e)}"}]

            notebooks_data.append({
                'title': item['title'],
                'type': item['type'],
                'date': '2026',
                'outputs': outputs_collected if outputs_collected else [{'type': 'text', 'content': 'No execution outputs found in notebook cells.'}]
            })

        context['notebooks_data'] = notebooks_data
        return context

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import TrafficSensorReading

# 1. Traffic List Function-Based View
def traffic_list(request):
    fwy_filter = request.GET.get('fwy', '')
    readings = TrafficSensorReading.objects.all().order_by('-hour')

    if fwy_filter:
        readings = readings.filter(fwy=fwy_filter)

    paginator = Paginator(readings, 25)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'govsim/traffic_list.html', {
        'page_obj': page_obj,
        'freeways': TrafficSensorReading.objects.values_list('fwy', flat=True).distinct(),
        'selected_fwy': fwy_filter,
    })

# 2. Traffic JSON API Endpoint
def traffic_data_api(request):
    """JSON endpoint for JS-driven charts/filters."""
    readings = TrafficSensorReading.objects.all().order_by('-hour')[:500]
    data = list(readings.values('hour', 'fwy', 'name', 'speed_mph', 'occupancy_pct', 'city'))
    return JsonResponse({'events': data}, safe=False)

# 3. Notebook Dashboard Class-Based View
#class AutoMatrixDashboardView(TemplateView):
#    template_name = 'govsim/traffic_matrix_dashboard.html'