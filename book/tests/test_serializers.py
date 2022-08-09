from django.test import TestCase

from book.models import Book
from book.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book1 = Book.objects.create(name='Test book 1', price=100)
        book2 = Book.objects.create(name='Test book 2', price=150)
        data = BooksSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Test book 1',
                'price': 100,
            },
            {
                'id': book2.id,
                'name': 'Test book 2',
                'price': 150,
            },
        ]

        self.assertEqual(expected_data, data)