from django.test import TestCase

from muddle.settings import register, AppSettings
from muddle.settings.registration import SETTINGS, Category, Subcategory
from muddle.settings.models import AppSettingsCategory, AppSettingsValue
from muddle.tests.forms import Foo, Bar, Xoo


__all__ = ['AppSettingsUsage']


class AppSettingsUsageBase(TestCase):
    """
    Base class for TestCases that need an initial set of settings registered
    """

    def setUp(self):
        self.tearDown()

        register('general', Foo, 'foo')
        register('general', Bar, 'foo')
        register('general', Xoo, 'xoo')

        category = AppSettingsCategory.objects.create(name='general.foo')
        AppSettingsValue.objects.create(category=category, key='two', data='two!')
        AppSettingsValue.objects.create(category=category, key='three', data='three!')

    def tearDown(self):
        SETTINGS.clear()
        AppSettingsCategory.objects.all().delete()
        AppSettingsValue.objects.all().delete()


class AppSettingsUsage(AppSettingsUsageBase):

    def test_get_top_level_category(self):
        category = AppSettings.general
        self.assertTrue(isinstance(category, (Category,)))

    def test_get_subcategory(self):
        subcategory = AppSettings.general.foo
        self.assertTrue(isinstance(subcategory, (Subcategory,)))

        # subcategories should not be cached
        same_category = AppSettings.general.foo
        self.assertNotEqual(id(subcategory), id(same_category))

    def test_get_value(self):
        self.assertEqual('two!', AppSettings.general.foo.two)
        self.assertEqual('three!', AppSettings.general.foo.three)

    def test_set_value(self):
        AppSettings.general.foo.two = 'new two!'
        self.assertEqual('new two!', AppSettings.general.foo.two)