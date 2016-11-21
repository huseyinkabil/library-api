from django.conf.urls import url
from main.views.library_views import LibraryView

app_name = 'main'
urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='library'),
]
