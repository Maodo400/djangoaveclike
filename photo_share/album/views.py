from typing import Any, Dict
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .forms import AlbumCreationForm, AlbumImageUploadForm
from .models import Album, AlbumImage
from user.models import User


class AlbumCreationView(CreateView):
    """Use this view to create new photo albums"""
    model = Album
    template_name = 'album/create-album.html'
    form_class = AlbumCreationForm

    def get_success_url(self) -> str:
        return reverse_lazy('user:profile', args=[self.request.user.slug])


class AlbumsView(ListView):
    """Use this view to list all albums of the profile user"""
    model = Album
    template_name = 'album/albums.html'
    context_object_name = 'albums'

    def get_queryset(self):
        # Get the user's slug field of the profile that is being viewed
        user = self.kwargs['slug']
        # Return all albums that belong to the profile user
        # that is being viewed
        return Album.objects.filter(user__username=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the user object from the `slug` field in the url
        context["profile_user"] = User.objects.get(
            username=self.kwargs['slug'])
        return context


class AlbumView(DetailView):
    model = Album
    template_name = 'album/album.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = AlbumImage.objects.filter(
            album__id=self.kwargs['pk'])
        context['profile'] = User.objects.get(slug=self.kwargs['slug'])
        return context


class AlbumImageUploadView(CreateView):
    model = AlbumImage
    template_name = 'album/upload-image.html'
    # form_class = AlbumImageUploadForm

    fields = [
        'image',
    ]

    def get_success_url(self) -> str:
        return reverse_lazy('album:album', args=[self.request.user.slug, self.kwargs['pk']])

    def form_valid(self, form):
        # TODO Fix issue where the upload saves
        # the last image selected twice
        images = self.request.FILES.getlist('image')
        for image in images:
            AlbumImage.objects.create(
                image=image,
                album=Album.objects.get(pk=self.kwargs['pk']),
                user=self.request.user
            )
            form.instance.user = self.request.user
            form.instance.album = Album.objects.get(pk=self.kwargs['pk'])

        return super().form_valid(form)
