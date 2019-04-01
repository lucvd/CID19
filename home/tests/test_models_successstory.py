from django.test import TestCase

from home.models import SuccessStory

class SuccessStoryTestCase(TestCase):
    def test_successtory_str(self):
        story = SuccessStory.objects.create(title="Test", subtitle="ook test", website="www.test.com", abstract="uitleg")
        self.assertEqual(str(story), "Test", "The __str__ method should return the title, as this is used in UI components")
