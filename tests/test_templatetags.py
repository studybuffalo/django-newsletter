"""Tests for the templatetags module."""
from io import BytesIO
from shutil import rmtree

# Conditionally import for Python 2.7 support
try:
    from tempfile import TemporaryDirectory as TempDir
except ImportError:
    import tempfile
    TempDir = None

from PIL import Image

from django.core.files.base import File
from django.template import Context, Template
from django.test import override_settings

from newsletter.models import (
    Newsletter, Message, Article, get_default_sites
)

from .utils import MailTestCase


class TemporaryDirectory:
    """Mimicks TemporaryDirectory to give Python 2 and 3 support."""
    def __init__(self):
        if TempDir:
            temp_dir = TempDir()
            self.name = temp_dir.name
        else:
            self.name = tempfile.mkdtemp()

    def __exit__(self, exc, value, traceback):
        rmtree(self.name)

# Create temporary directory for created media files
TEMP_DIR = TemporaryDirectory()
TEMP_DIR_PATH = TEMP_DIR.name

@override_settings(MEDIA_ROOT=TEMP_DIR_PATH)
class ArticleTestCase(MailTestCase):
    def get_newsletter_kwargs(self):
        """ Returns the keyword arguments for instanciating the newsletter. """
        return {
            'title': 'Test newsletter',
            'slug': 'test-newsletter',
            'sender': 'Test Sender',
            'email': 'test@testsender.com'
        }

    def create_test_image(self):
        # Create Bytes object to hold image in memory
        image_file = BytesIO()

        # Create a 600 x 600 px image and save to bytes object
        image = Image.new('RGB', size=(600, 600), color=(256, 0, 0))
        image.save(image_file, 'png')

        # Return file pointer to start to allow proper reading
        image_file.seek(0)

        # Return image as a Django File object
        return File(image_file, name='test-image.png')

    def setUp(self):
        # Create newsletter for testing
        self.newsletter = Newsletter.objects.create(
            **self.get_newsletter_kwargs()
        )
        self.newsletter.site.set(get_default_sites())

        # Add a message to the newsletter
        self.message = Message.objects.create(
            title='Test message',
            newsletter=self.newsletter,
            slug='test-message',
        )

        # Add an article to message
        self.article = Article.objects.create(
            title='Test title',
            text='This is the article text.',
            post=self.message,
            image=self.create_test_image(),
        )

    def test_tag_outputs_thubmnail_url(self):
        """Confirms an expected image URL is provided."""
        template = Template(
            '{% load newsletter_thumbnails %}'
            '{% for article in message.articles.all %}'
            '{% newsletter_thumbnail article.image as thumbnail %}'
            '{{ thumbnail }}'
            '{% endfor %}'
        ).render(
            Context({'message': self.message})
        )

        # TODO: Update to assertRegex when Python 2.7 support dropped
        self.assertRegexpMatches(
            template,
            r'newsletter(\/|\\)images(\/|\\).*test-image.*_thumbnail\.png'
        )
