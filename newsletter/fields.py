"""Custom Django model fields."""
import os
from io import BytesIO

from PIL import Image

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models.fields.files import ImageField, ImageFieldFile


class ThumbnailImageFile(ImageFieldFile):
    """Provides methods to generate & retrieve thumbnails."""
    def _create_thumbnail_file_path(self, file_name):
        """Creates path for thumbnail.

            Recreates the original image's media folder so it can
            uploaded to the same folder.
        """
        # Break path into head and tail
        image_folders, full_image_name = os.path.split(file_name)

        # Break image name into the name and extension
        image_name, image_extension = os.path.splitext(full_image_name)

        # Break the path head into individual folders
        image_folder_parts = str(image_folders).split(os.path.sep)

        # Reconstruct the media folder for the original image
        # Will need the last 5 parts (all files are uploaded with the
        # same structure: newsletter/images/<year>/<month>/<day>)
        media_folder_path = image_folder_parts[-5:]

        # Combine media path parts and image name
        thumbnail_path_parts = media_folder_path + [image_name]

        # Return the joined path and thumbnail name
        return '%s_thumbnail%s' % (
            os.path.sep.join(thumbnail_path_parts), image_extension
        )

    def thumbnail(self):
        """Resizes, saves, and retrieves thumbnails."""
        # Get the thumbnail path
        thumbnail_path = self._create_thumbnail_file_path(self.file.name)

        # Check if thumbnail needs to be created
        if default_storage.exists(thumbnail_path) is False:
            # Create bytes object to hold the thumbnail in memory
            thumbnail_io = BytesIO()

            # Open the image and resize it
            original_image = Image.open(self.file)
            original_image.thumbnail((128, 128))

            # Save the image to the bytes object
            original_image.save(thumbnail_io, format='JPEG')

            # Save the bytes object as a Django File
            default_storage.save(
                thumbnail_path, ContentFile(thumbnail_io.getvalue())
            )

        return default_storage.url(thumbnail_path)

class ThumbnailImageField(ImageField):
    """Updated image field to provide thumbnail handling."""
    attr_class = ThumbnailImageFile
