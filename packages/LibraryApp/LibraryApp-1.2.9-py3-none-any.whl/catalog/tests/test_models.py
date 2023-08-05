import datetime
from django.utils import timezone
from catalog.models import Author
from django.urls import reverse
from catalog.models import Book
from catalog.models import Language
from catalog.models import BookInstance
from catalog.models import Genre
from datetime import date
from django.test import TestCase


class AuthorModelTest(TestCase):
    # Setup test data, then test author labels.

    # This decorator will allow us to call that method
    # using the class name instead of the object.
    # In below example, the setUpTestData has one parameter
    # cls, which refers to the AuthorModelTest class.
    # now we can call the setUpTestData method using
    # AuthorModelTest.setUpTestData()
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Kevin', last_name='Kithinji', id=1)

    def test_first_name_label(self):
        # Get the author object to test
        author = Author.objects.get(id=1)
        # Get the metadata for the required field
        # and use it to query the required field data
        field_label = author._meta.get_field('first_name').verbose_name
        # Compare the value to the expected result
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(
            author.last_name, author.first_name)

        self.assertEqual(expected_object_name, str(author))


class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='test_genre', id=1)

    def test_str_is_equal_to_title(self):
        genre = Genre.objects.get(id=1)
        self.assertEqual(str(genre), genre.name)


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Mr', last_name='Testy', id=1)
        author = Author.objects.get(id=1)
        Language.objects.create(name='Klingon')
        testLang = Language.objects.get(id=1)
        Genre.objects.create(name='test_genre', id=1)
        genres = Genre.objects.all()
        bk = Book.objects.create(title='TestyBook', author=author,
                                 summary='testysummary', isbn='872727727',
                                 language=testLang)
        bk.genre.set(genres)
        title = Book.objects.get(id=1)
        BookInstance.objects.create(book=title, imprint='testimprint',
                                    id=1)

    def test_book_title_label(self):
        title = Book.objects.get(id=1)
        field_label = title._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_isbn_label(self):
        isbn = Book.objects.get(id=1)
        field_label = isbn._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_author_name_label(self):
        author = Book.objects.get(id=1)
        field_label = author._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_language_name_label(self):
        language = Book.objects.get(id=1)
        field_label = language._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_str_is_equal_to_name(self):
        example = Book.objects.get(id=1)
        self.assertEqual(str(example), example.title)


class test_book_instance(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Mr', last_name='Testy', id=1)
        author = Author.objects.get(id=1)
        Language.objects.create(name='Klingon', id=1)
        testLang = Language.objects.get(id=1)
        Book.objects.create(title='TestyBook', author=author,
                            summary='testysummary', isbn='872727727',
                                    language=testLang, id=1)
        title = Book.objects.get(id=1)
        time = timezone.now() + datetime.timedelta(days=30)
        time_2 = timezone.now() - datetime.timedelta(days=30)
        BookInstance.objects.create(book=title, imprint='testimprint',
                                    due_back=time, id=1)
        BookInstance.objects.create(book=title, imprint='testimprint',
                                    due_back=time_2, id=2)

    def test_book_isnt_overdue(self):
        book_instance = BookInstance.objects.get(id=1)
        isnt_due = book_instance.due_back and date.today(
        ) > book_instance.due_back
        self.assertIs(isnt_due, False)

    def test_book_is_overdue(self):
        book_instance = BookInstance.objects.get(id=2)
        is_due = book_instance.due_back and date.today(
        ) > book_instance.due_back
        self.assertIs(is_due, True)

    def test_str_is_equal_to_name(self):
        example = BookInstance.objects.get(id=1)
        expected_object_name = '{0} ({1})'.format(
            example.id, example.book.title)
        self.assertEqual(expected_object_name, str(example))


class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name='Klingon', id=1)

    def test_language_label(self):
        name = Language.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_str_is_equal_to_name(self):
        example = Language.objects.get(pk=1)
        self.assertEqual(str(example), example.name)
