from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from .views import bidding_process_detail, bidders_list
from . import views
from django.conf.urls.static import static
from . import bidding_process_api


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', views.landingpage, name='landingpage'),
    path('properties/<int:property_id>/bidders/', bidders_list, name='bidders_list'),
    path('properties/<int:property_id>/bidding_process/', bidding_process_detail, name='bidding_process_detail'),
    path('api/bidding-process/create/', bidding_process_api.create_bidding_process, name='create_bidding_process'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)