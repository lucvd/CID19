from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta

import unittest


class jenkinsunittest(TestCase):
    def test_alwaystrue(self):
        self.assertEqual('foo'.upper(), 'FOO')