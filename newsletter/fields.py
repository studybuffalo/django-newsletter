from django.db.models import ImageField

from .settings import newsletter_settings

# If a thumbnail class as set and successfully imported, will use it
# Otherwise will use the Django ImageField as the default fallback
if newsletter_settings.THUMBNAIL_MODEL_FIELD:
    ParentClass = newsletter_settings.THUMBNAIL_MODEL_FIELD
else:
    ParentClass = ImageField

DynamicImageField = type("DynamicImageField", (ParentClass,), {})
