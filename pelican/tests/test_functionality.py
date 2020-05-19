import unittest
import pytz

from pelican import utils
from pelican.contents import Page
from pelican.settings import read_settings
from pelican.urlwrappers import Author


class TestFunctionality(unittest.TestCase):
    def test_slugify_text(self):

        samples = (('slug slugi slugify', 'slug-slugi-slugify'),
                   ('slug        slugi slugify', 'slug-slugi-slugify'),
                   ('slug -> slugi -> slugify', 'slug-slugi-slugify'),
                   ('slug--slugi--slugify', 'slug-slugi-slugify'),
                   )

        settings = read_settings()
        substitute = settings['SLUG_REGEX_SUBSTITUTIONS']

        for value, expected in samples:
            self.assertEqual(utils.slugify(value, regex_subs=substitute), expected)

    def test_get_date_returns_correct_value(self):
        date = utils.SafeDatetime(year=2020, month=0o4, day=30)
        date_hour = utils.SafeDatetime(
            year=2020, month=0o4, day=30, hour=20, minute=10
        )
        date_hour_utc = utils.SafeDatetime(
            year=2020, month=0o4, day=30, hour=20, minute=10,
            tzinfo=pytz.timezone('UTC')
        )
        date_hour_est = utils.SafeDatetime(
            year=2020, month=0o4, day=30, hour=20, minute=10,
            tzinfo=pytz.timezone('EST')
        )
        date_hour_seconds = utils.SafeDatetime(
            year=2020, month=0o4, day=30, hour=20, minute=10, second=20,
        )
        date_hour_seconds_utc = utils.SafeDatetime(
            year=2020, month=0o4, day=30, hour=20, minute=10, second=20,
            tzinfo=pytz.timezone('UTC')
        )
        date_hour_seconds_est = utils.SafeDatetime(
            year=2020, month=0o4, day=30, hour=20, minute=10, second=20,
            tzinfo=pytz.timezone('EST')
        )
        date_hour_seconds_usecs_utc = utils.SafeDatetime(
            year=2020, month=0o4, day=30, hour=20, minute=10, second=20,
            microsecond=123000, tzinfo=pytz.timezone('UTC')
        )

        dates = {
            '2020/04/30': date,
            '2020-04-30': date,
            '30/04/2020': date,
            '30-04-2020': date,
            '30.04.2020': date,
            '2020/04/30 20:10': date_hour,
            '2020-04-30 20:10': date_hour,
            '30.04.2020 20:10': date_hour,
            '2020-04-30T20:10Z': date_hour_utc,
            '2020-04-30T20:10-0500': date_hour_est,
            '2020/04/30 20:10:20': date_hour_seconds,
            '2020-04-30T20:10:20Z': date_hour_seconds_utc,
            '2020/04/30T20:10:20-0500': date_hour_seconds_est,
            '2020-04-30T20:10:20.123Z': date_hour_seconds_usecs_utc,
        }

        # ISO 8601 datetime format
        iso_8601_date = utils.SafeDatetime(
            year=1997, month=7, day=15,
        )
        iso_8601_date_hour_timezone = utils.SafeDatetime(
            year=1997, month=7, day=15, hour=19, minute=20,
            tzinfo=pytz.timezone('CET')
        )
        iso_8601_date_hour_secs_timezone = utils.SafeDatetime(
            year=1997, month=7, day=15, hour=19, minute=20, second=30,
            tzinfo=pytz.timezone('CET')
        )
        iso_8601_date_hour_secs_ms = utils.SafeDatetime(
            year=1997, month=7, day=15, hour=19, minute=20, second=30,
            microsecond=120000, tzinfo=pytz.timezone('CET')
        )

        iso_8601_format = {
            '1997-07-15': iso_8601_date,
            '1997-07-15T19:20+01:00': iso_8601_date_hour_timezone,
            '1997-07-15T19:20:30+01:00': iso_8601_date_hour_secs_timezone,
            '1997-07-15T19:20:30.12+01:00': iso_8601_date_hour_secs_ms,
        }

        # Invalid dates
        invalid_dates =['2040-123-3,' 'wrongdate', '2.12.ac', '001/1001']

        for value, expected in dates.items():
            self.assertEqual(utils.get_date(value), expected, value)
            self.assertTrue(utils.get_date(value) is not None)

        for value, expected in iso_8601_format.items():
            self.assertEqual(utils.get_date(value), expected, value)

        for date in invalid_dates:
            self.assertRaises(ValueError, utils.get_date, date)

    def test_props_must_exist(self):
        page = Page('content')
        self.assertFalse(page._has_valid_mandatory_properties())
        new_page = Page('content', metadata={'title': 'Pelican'})
        self.assertTrue(new_page._has_valid_mandatory_properties())

    def test_set_default_language(self):
        self.page_kwargs = {
            'content': 'Content',
            'context': {
                'localsiteurl': '',
            },
            'metadata': {
                'summary': 'Summary',
                'title': 'Title',
                'author': Author('Blogger', 'settings')
            }
        }
        page = Page(**self.page_kwargs)
        self.page_kwargs['metadata'].update({'lang': 'en'})
        page = Page(**self.page_kwargs)
        self.assertEqual(page.lang, 'en')

    def test_article_with_more_than_one_authors(self):
        self.page_kwargs = {
            'content': 'Content',
            'context': {
                'localsiteurl': '',
            },
            'metadata': {
                'summary': 'Summary',
                'title': 'Title',
                'author': Author('Tom', 'settings')
            }
        }
        args = self.page_kwargs.copy()
        content = Page(**args)
        assert content.authors == [content.author]

        args['metadata'].pop('author')
        args['metadata']['authors'] = [Author('Tom', 'DEFAULT'),
                                       Author('Jeff', 'DEFAULT'),
                                       Author('Sean', 'DEFAULT')]
        content = Page(**args)
        self.assertTrue(content.authors)
