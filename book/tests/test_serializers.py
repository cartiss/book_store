from django.test import TestCase

from book.models import Book
from book.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(name='Test book 1', price=100, author='Author')
        self.book2 = Book.objects.create(name='Test book 2', price=150, author='Author2')

    def test_ok(self):
        data = BooksSerializer([self.book1, self.book2], many=True).data
        expected_data = [
            {
                'id': self.book1.id,
                'name': 'Test book 1',
                'price': 100,
                'author': 'Author'
            },
            {
                'id': self.book2.id,
                'name': 'Test book 2',
                'price': 150,
                'author': 'Author2'
            },
        ]

        self.assertEqual(expected_data, data)