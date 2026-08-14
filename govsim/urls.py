from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'govsim'

urlpatterns = [
    path('', views.AdListView.as_view(), name='home'),
    path('index/', views.AdListView.as_view(), name='all'),
    path('traffic-matrix-dashboard/', views.AutoMatrixDashboardView.as_view(), name='traffic_matrix_dashboard'),
    path('traffic-list/', views.traffic_list, name='traffic_list'),
    path('api/data/', views.traffic_data_api, name='traffic_data_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
