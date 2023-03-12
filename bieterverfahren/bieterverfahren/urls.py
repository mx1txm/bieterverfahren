from django.contrib import admin
from django.urls import include, path
from .views import bidding_process_detail, bidders_list
from django.views.generic import (  # TODO: remove once real views are present
    TemplateView,
)


# TODO: remove once real views are present
class ExampleView(TemplateView):
    template_name = "landingpage.html"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", ExampleView.as_view()),
    path('properties/<int:property_id>/bidders/', bidders_list, name='bidders_list'),
    path('properties/<int:property_id>/bidding_process/', bidding_process_detail, name='bidding_process_detail'),
]
