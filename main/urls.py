from django.conf.urls import url
from main.views.library_views import LibraryView
from main.views.book_views import BookView
from main.views.author_views import AuthorView


app_name = 'main'
urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^book/$', BookView.as_view(), name='book'),
    url(r'^book/(?P<id>[0-9]+)/$', BookView.as_view(), name='book'),
    url(r'^author/$', AuthorView.as_view(), name='author'),
    url(r'^author/(?P<id>[0-9]+)/$', AuthorView.as_view(), name='author'),
]
