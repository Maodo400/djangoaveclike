from django import forms
from .models import Image, ImageLikes
from utils.forms.widgets import text_input, select_input, image_input


class ImageUploadForm(forms.ModelForm):
    """Use this form to upload images"""

    class Meta:
        model = Image

        fields = [
            "name",
            "image",
            "status",
        ]

        widgets = {
            "name": text_input,
            "image": image_input,
            "status": select_input,
        }
