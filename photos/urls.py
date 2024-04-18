from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = "photos"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("photos/<slug:slug>/upload/", views.ImageUploadView.as_view(), name="upload"),
    path("photos/<slug:slug>/image/<int:pk>/", views.ImageView.as_view(), name="image"),
    path(
        "photos/<slug:slug>/image/<int:pk>/delete/",
        views.DeleteImageView.as_view(),
        name="delete",
    ),
    path(
        "photos/<slug:slug>/image/<int:pk>/update/",
        views.UpdateImageView.as_view(),
        name="update",
    ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
