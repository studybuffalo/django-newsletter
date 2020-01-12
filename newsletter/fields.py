"""Custom Django model fields."""
from django.db.models import ImageField


class ThumbnailImageField(ImageField):
    """Updated image field to handle resizing images for thumbnails."""
    def thumbnail(self):
        """Generates and/or returns a thumbnail image."""
        original_image = getattr(self, self.attname)
        image_name = original_image.name

        # Create file name for this image
        # Get file name, extension
        # Add _thumbnail

        # Attempt to retrieve image; if does not exist, create it

