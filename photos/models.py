from django.db import models
from django.urls import reverse
from user.models import User


class Image(models.Model):
    """This model holds information for user uploaded images"""

    # Status of the image
    class Status(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"

    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to="images/")
    status = models.CharField(
        max_length=7, choices=Status.choices, default=Status.PUBLIC
    )
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("photos:image", kwargs={"slug": self.user.slug, "pk": self.pk})

    class Meta:
        indexes = [
            models.Index(fields=["name"], name="name_idx"),
            models.Index(fields=["user"], name="user_idx"),
        ]

        ordering = ["-upload_date"]


class ImageLikes(models.Model):
    """This model stores information about likes for a image object."""

    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="image_likes")

    def __str__(self) -> str:
        return self.image.name

