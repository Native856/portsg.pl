from django.urls import path, include
from . import views
from .views import BookUpdateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'BookApp'

urlpatterns = [
    path('', views.base, name='base'),
    path('book_table', views.book_filter_views, name='book_table'),
    path('book_detail/<int:pid>/<slug:slug>/<str:author>/<int:year>/', views.book_detail_views, name='book_detail'),
    path('book_add', views.book_add_views, name='book_add'),
    path('<pk>/update', BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>', views.book_delete_views, name='delete_book'),
    path('book_import', views.book_api_views, name='book_import'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
