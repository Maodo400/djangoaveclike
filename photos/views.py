from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .models import Image, ImageLikes
from .forms import ImageUploadForm


class IndexView(ListView):
    model = Image
    template_name = "index.html"
    context_object_name = "images"

    def get_queryset(self):
        """Display `public` photos only"""
        return Image.objects.filter(status=Image.Status.PUBLIC)


class ImageUploadView(CreateView):
    """Use this view to upload images"""

    model = Image
    template_name = "photos/upload.html"
    form_class = ImageUploadForm

    def get_success_url(self) -> str:
        return reverse_lazy("user:profile", args=[self.request.user.slug])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class UpdateImageView(UpdateView):
    """Use this view to update images"""
    model = Image
    template_name = "photos/update.html"
    form_class = ImageUploadForm
    success_url = reverse_lazy("user:profile")

    def form_valid(self, form):
        # Retrieve the image object based on the provided ID
        image = self.get_object()
        # Update the image object's fields with the submitted form data
        form.instance.user = self.request.user  # If user needs to be updated
        # Save the changes
        return super().form_valid(form)

    def get_queryset(self):
        """Limit queryset to images owned by the current user"""
        return Image.objects.filter(user=self.request.user)

    def get_success_url(self) -> str:
        return reverse_lazy("user:profile", args=[self.request.user.slug])

class ImageView(DetailView):
    """Use this view to display a image object"""

    model = Image
    template_name = "photos/image.html"
    context_object_name = "image"


class DeleteImageView(DeleteView):
    """Use this view to delete images"""

    model = Image
    template_name = "photos/delete-image.html"
    context_object_name = "image"

    def get_success_url(self) -> str:
        return reverse_lazy("user:profile", args=[self.request.user.slug])

