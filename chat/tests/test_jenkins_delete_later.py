from django.test import TestCase


class jenkinsunittest(TestCase):
    def test_alwaystrue(self):
        self.assertEqual('foo'.upper(), 'FOO')