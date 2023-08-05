from django.test import TestCase


# Create your tests here.

import datetime
from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):

    def test_renew_form_date_in_past(self):
        # If renewal date is before today, then form is invalid. Test this
        # set date of previous day (ikue jana)
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        # Confirm that this test fails
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        # Test that if a renewal data is too
        # far in the future, it shouldnt go through
        date = datetime.date.today() + datetime.timedelta(
            weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        # If renewal date is today, then thats fine.
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        # If renewal date is within four weeks, form is okay
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_field_label(self):
        """Test renewal_date label is 'renewal date'."""
        form = RenewBookForm()
        self.assertTrue(
            form.fields['renewal_date'].label is None or form.fields[
                'renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        """Test renewal_date help_text is as expected."""
        form = RenewBookForm()
        self.assertEqual(
            form.fields['renewal_date'].help_text,
            'Enter a date between now and 4 weeks (default 3).')
